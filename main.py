#!/usr/bin/env python3

import os
import sys
from pathlib import Path

from civitai_manager.core.metadata_manager import (
    VERSION,
    process_single_file,
    process_directory,
    clean_output_directory,
    generate_image_json_files,
    get_output_path
)
from src.civitai_manager.utils.html_generators.browser_page import generate_global_summary
from src.civitai_manager.utils.config import Config, load_config, ConfigValidationError

import argparse
import typed_argparse as tap

class CommonArgs(tap.TypedArgs):
    notimeout: bool
    output: str = tap.arg(help='Output directory path (if not specified, will prompt for it)', default="out")
    images: bool = tap.arg(help='Download all available preview images instead of just the first one', default=False)
    generateimagejson: bool = tap.arg(help='Generate JSON files for all preview images from existing model version data', default=False)
    noimages: bool = tap.arg(help='Skip downloading any preview images', default=False)
    onlynew: bool = tap.arg(help='Only process new files that haven\'t been processed before', default=False)
    skipmissing: bool = tap.arg(help='Skip previously missing models when used with --onlynew', default=False)
    onlyhtml: bool = tap.arg(help='Only generate HTML files from existing JSON data', default=False)
    onlyupdate: bool = tap.arg(help='Only update previously processed files, skipping hash calculation', default=False)
    clean: bool = tap.arg(help='Remove data for models that no longer exist in the target directory', default=False)
    noconfig: bool = tap.arg(help='Ignore config.json and use command line arguments only', default=False)
    single: str | None = tap.arg(help='Path to a single .safetensors file', default=None)
    all: str | None = tap.arg(help='Path to directory containing .safetensors files', default=None)
    api_key: str | None = tap.arg(help='API key for Civitai API', default=None)
    use_swarm: bool = tap.arg(help='Use Swarm API to fetch model data', default=False)

def parse_cli_args(require_args: bool=False):
    """Parse and validate command line arguments."""
    parser = argparse.ArgumentParser(description='Process SafeTensors files and fetch Civitai data')
    group = parser.add_mutually_exclusive_group(required=require_args)
    _ = group.add_argument('--single', type=str, help='Path to a single .safetensors file')
    _ = group.add_argument('--all', type=str, help='Path to directory containing .safetensors files')
    _ = parser.add_argument('--notimeout', action='store_true', 
                       help='Disable timeout between files (warning: may trigger rate limiting)')
    _ = parser.add_argument('--output', type=str, default="out",
                       help='Output directory path (if not specified, will prompt for it)')
    _ = parser.add_argument('--images', action='store_true',
                       help='Download all available preview images instead of just the first one')
    _ = parser.add_argument('--generateimagejson', action='store_true',
                       help='Generate JSON files for all preview images from existing model version data')
    _ = parser.add_argument('--noimages', action='store_true',
                       help='Skip downloading any preview images')
    _ = parser.add_argument('--onlynew', action='store_true',
                       help='Only process new files that haven\'t been processed before')
    _ = parser.add_argument('--skipmissing', action='store_true',
                       help='Skip previously missing models when used with --onlynew')
    _ = parser.add_argument('--onlyhtml', action='store_true',
                       help='Only generate HTML files from existing JSON data')
    _ = parser.add_argument('--onlyupdate', action='store_true',
                       help='Only update previously processed files, skipping hash calculation')
    _ = parser.add_argument('--clean', action='store_true',
                       help='Remove data for models that no longer exist in the target directory')
    _ = parser.add_argument('--noconfig', action='store_true',
                       help='Ignore config.json and use command line arguments only')
    _ = parser.add_argument('--api-key', type=str,
                       help='API key for Civitai API')
    _ = parser.add_argument('--use-swarm', action='store_true',
                       help='Use Swarm API to fetch model data')


    inargs = parser.parse_args()
    args = CommonArgs.from_argparse(inargs)
    
    # Validate arguments
    if args.images and args.noimages:
        print("Error: Cannot use both --images and --noimages at the same time")
        sys.exit(1)
    if args.onlynew and args.onlyhtml:
        print("Error: Cannot use both --onlynew and --onlyhtml at the same time")
        sys.exit(1)
    if args.onlyupdate and args.onlynew:
        print("Error: Cannot use both --onlyupdate and --onlynew at the same time")
        sys.exit(1)
    if args.onlyupdate and args.onlyhtml:
        print("Error: Cannot use both --onlyupdate and --onlyhtml at the same time")
        sys.exit(1)
    # if args.clean and isinstance(args, ArgsSingle):
    #     print("Error: --clean option can only be used with --all")
    #     sys.exit(1)
    # if args.clean and (args.onlyhtml or args.onlyupdate or args.onlynew):
    #     print("Error: --clean cannot be used with --onlyhtml, --onlyupdate, or --onlynew")
    #     sys.exit(1)

    return args

def get_config() -> Config:
    """
    Try to load config from file first, fall back to CLI args if no config found
    or if config is invalid. Respect --noconfig flag.
    """
    # First check if --noconfig is specified without requiring other arguments
    args = parse_cli_args(require_args=False)
    
    if not args.noconfig:
        print("Attempting to load config.json...")
        try:
            config = load_config()
            if config:
                print("Successfully loaded configuration from config.json")
                print(f"Config contents: {config}")
                return config
        except ConfigValidationError as e:
            print(f"Error in config file: {str(e)}")
        except Exception as e:
            print(f"Error loading config file: {str(e)}")
    else:
        print("Using command line arguments (--noconfig specified)")
    
    # If we get here, either --noconfig was used or config loading failed
    # Now we require CLI arguments
    args = parse_cli_args(require_args=True)
    return Config.model_validate(args)

def main():
    config = get_config()
    
    # Get base output path either from config/argument or user input
    if config.output:
        if not config.output.exists():
            try:
                config.output.mkdir(parents=True, exist_ok=True)
                print(f"Created output directory: {config.output}")
            except Exception as e:
                print(f"Error creating output directory: {str(e)}")
                sys.exit(1)
        if not os.access(config.output, os.W_OK):
            print(f"Error: No write permission for directory {config.output}")
            sys.exit(1)
    else:
        config.output = get_output_path(clean=config.clean)
    
    if config.single:
        safetensors_path = Path(config.single)
        _ = process_single_file(config, safetensors_path)
    elif config.all:
        directory_path = Path(config.all)
        
        if config.clean:
            _ = clean_output_directory(directory_path, config.output)
        elif config.generateimagejson:
            _ = generate_image_json_files(config.output)
        else:
            _ = process_directory(config, directory_path)
        
    if (config.single or config.all):
        _ = generate_global_summary(config.output, VERSION)

if __name__ == "__main__":
    main()

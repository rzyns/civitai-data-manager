#!/usr/bin/env python3

import os
import sys
import argparse
from pathlib import Path
from src.civitai_manager.core.metadata_manager import (
    VERSION,
    process_single_file,
    process_directory,
    get_output_path
)
from src.civitai_manager.utils.html_generators.browser_page import generate_global_summary

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Process SafeTensors files and fetch Civitai data')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--single', type=str, help='Path to a single .safetensors file')
    group.add_argument('--all', type=str, help='Path to directory containing .safetensors files')
    parser.add_argument('--notimeout', action='store_true', 
                       help='Disable timeout between files (warning: may trigger rate limiting)')
    parser.add_argument('--output', type=str, 
                       help='Output directory path (if not specified, will prompt for it)')
    parser.add_argument('--images', action='store_true',
                       help='Download all available preview images instead of just the first one')
    parser.add_argument('--noimages', action='store_true',
                       help='Skip downloading any preview images')
    parser.add_argument('--onlynew', action='store_true',
                       help='Only process new files that haven\'t been processed before')
    parser.add_argument('--onlyhtml', action='store_true',
                       help='Only generate HTML files from existing JSON data')
    parser.add_argument('--onlyupdate', action='store_true',
                       help='Only update previously processed files, skipping hash calculation')

    args = parser.parse_args()
    
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
    
    # Get base output path either from argument or user input
    if args.output:
        base_output_path = Path(args.output)
        if not base_output_path.exists():
            try:
                base_output_path.mkdir(parents=True, exist_ok=True)
                print(f"Created output directory: {base_output_path}")
            except Exception as e:
                print(f"Error creating output directory: {str(e)}")
                sys.exit(1)
        if not os.access(base_output_path, os.W_OK):
            print(f"Error: No write permission for directory {base_output_path}")
            sys.exit(1)
    else:
        base_output_path = get_output_path()
    
    if args.single:
        safetensors_path = Path(args.single)
        process_single_file(safetensors_path, base_output_path, 
                          download_all_images=args.images,
                          skip_images=args.noimages,
                          html_only=args.onlyhtml,
                          only_update=args.onlyupdate)
    else:
        directory_path = Path(args.all)
        process_directory(directory_path, base_output_path, 
                        args.notimeout,
                        download_all_images=args.images,
                        skip_images=args.noimages,
                        only_new=args.onlynew,
                        html_only=args.onlyhtml,
                        only_update=args.onlyupdate)
        
    if (args.single or args.all):
        generate_global_summary(base_output_path, VERSION)

if __name__ == "__main__":
    main()
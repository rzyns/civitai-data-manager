import json
from pathlib import Path

import pydantic

class Config(pydantic.BaseModel):
    single: str | None      = pydantic.Field(default=None)
    all: str | None         = pydantic.Field(default=None)
    output: pydantic.NewPath | pydantic.DirectoryPath = pydantic.Field(default_factory=Path)
    notimeout: bool         = pydantic.Field(default=False)
    images: bool            = pydantic.Field(default=True)
    generateimagejson: bool = pydantic.Field(default=False)
    noimages: bool          = pydantic.Field(default=False)
    onlynew: bool           = pydantic.Field(default=False)
    skipmissing: bool       = pydantic.Field(default=False)
    onlyhtml: bool          = pydantic.Field(default=False)
    onlyupdate: bool        = pydantic.Field(default=False)
    clean: bool             = pydantic.Field(default=False)
    api_key: str | None     = pydantic.Field(default=None)
    use_swarm: bool         = pydantic.Field(default=False)


ConfigTA = pydantic.TypeAdapter(Config)


class ConfigValidationError(Exception):
    pass

def validate_config(config: dict[str, object]) -> Config:
    """Validates the configuration and returns a normalized config dict."""
    # Required: either single or all path
    if not ('single' in config) ^ ('all' in config):  # XOR - exactly one must be present
        raise ConfigValidationError("Config must specify either 'single' or 'all' path, but not both")
    
    # Convert paths to strings if they're not already
    if 'single' in config:
        config['single'] = str(config['single'])
    if 'all' in config:
        config['all'] = str(config['all'])
    if 'output' in config:
        config['output'] = str(config['output'])

    # Boolean flags
    bool_flags = [
        'notimeout', 'images', 'generateimagejson', 'noimages', 'onlynew',
        'skipmissing', 'onlyhtml', 'onlyupdate', 'clean'
    ]
    for flag in bool_flags:
        if flag in config and not isinstance(config[flag], bool):
            raise ConfigValidationError(f"'{flag}' must be a boolean value")

    # Validate conflicting options - same checks as CLI arguments
    if config.get('images', False) and config.get('noimages', False):
        raise ConfigValidationError("Cannot use both 'images' and 'noimages' at the same time")
    
    if config.get('onlynew', False) and config.get('onlyhtml', False):
        raise ConfigValidationError("Cannot use both 'onlynew' and 'onlyhtml' at the same time")
    
    if config.get('onlyupdate', False) and config.get('onlynew', False):
        raise ConfigValidationError("Cannot use both 'onlyupdate' and 'onlynew' at the same time")
    
    if config.get('onlyupdate', False) and config.get('onlyhtml', False):
        raise ConfigValidationError("Cannot use both 'onlyupdate' and 'onlyhtml' at the same time")
    
    if config.get('clean', False):
        if 'single' in config:
            raise ConfigValidationError("'clean' option can only be used with 'all'")
        if any(config.get(opt, False) for opt in ['onlyhtml', 'onlyupdate', 'onlynew']):
            raise ConfigValidationError("'clean' cannot be used with 'onlyhtml', 'onlyupdate', or 'onlynew'")

    return ConfigTA.validate_python(config)

def load_config(config_path: str | Path | None = None) -> Config | None:
    """
    Load and validate configuration from a JSON file.
    If no path is provided, looks for 'config.json' in the script directory.
    Returns None if no config file is found.
    """
    if config_path is None:
        # Get the absolute path to the project root directory
        project_root = Path.cwd()
        config_path = project_root / 'config.json'
        import sys
        _ = sys.stderr.write(f"Looking for config at: {config_path.absolute()}\n")
        _ = sys.stderr.flush()
    else:
        config_path = Path(config_path)

    if not config_path.exists():
        import sys
        _ = sys.stderr.write(f"Config file not found at: {config_path}\n")
        _ = sys.stderr.flush()
        return None

    try:
        with open(config_path, 'r') as f:
            config = ConfigTA.validate_json(f.read())
        return config
    except json.JSONDecodeError as e:
        raise ConfigValidationError(f"Invalid JSON in config file: {str(e)}")
    except Exception as e:
        raise ConfigValidationError(f"Error loading config: {str(e)}")

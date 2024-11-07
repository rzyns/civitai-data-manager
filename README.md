# Civitai Data Manager

- [Overview](#overview)
- [Key Benefits](#key-benefits)
- [Model Compatibility](#model-compatibility)
- [Getting Started](#getting-started)
  - [Requirements](#requirements)
  - [Installation](#installation)
- [Usage Guide](#usage-guide)
  - [Basic Commands](#basic-commands)
  - [Additional Options](#additional-options)
  - [Recommended Organization](#recommended-organization)
  - [Best Practices](#best-practices)
- [Output Structure](#output-structure)
  - [Directory Layout](#directory-layout)
  - [Missing Models Tracking](#missing-models-tracking)
- [Features in Detail](#features-in-detail)
  - [Rate Limiting Protection](#rate-limiting-protection)
  - [Update Checking](#update-checking)
  - [HTML Generation](#html-generation)
  - [Processed Files Tracking](#processed-files-tracking)
- [Roadmap](#roadmap)
- [FAQ](#faq)
- [Additional Information](#additional-information)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Overview

A simple Python script that fetches and saves metadata, hashes, and preview images for SafeTensors model files by querying the Civitai API.

It generates JSON files for data storage and interactive HTML pages for easy browsing. The script is especially useful for maintaining model information (trigger words, usage notes, authors) even after models might be removed from Civitai. By creating a local backup of crucial model data, you can ensure your collection remains well-documented and easily accessible regardless of the models' availability online.

## Key Benefits

- **Save Trigger Words**: Preserve Lora trigger words even if the associated model is no longer available on Civitai.
- **Protect Key Information**: Models may be removed from Civitai, making it crucial to back up their usage instructions for future reference.
- **Minimalistic Tool**: A straightforward, lightweight solution that doesn't require installing a full Civitai manager on your computer.
- **Organize Model Details**: Keep track of model authors, versions, and usage examples for easy reference.
- **Monitor Unavailable Models**: Maintain a record of models you own that have been removed from Civitai.
- **Track All Downloads**: Easily manage models downloaded from Civitai, even if they've been renamed.
- **Smart Updates**: Updates only occur for models with new information on Civitai, keeping the process efficient.

## Model Compatibility

Works with all `.safetensors` files available on Civitai:
- Checkpoints
- Loras
- Control Net models
- ...

## Getting Started

### Requirements
- Python 3.6 or higher

### Installation

1. Clone the repository:
```bash
git clone https://github.com/jeremysltn/civitai-data-manager.git
```

2. Navigate to the project directory:
```bash
cd civitai-data-manager
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Make the script executable (Unix-like systems only):
```bash
chmod +x civitai_data_manager.py
```

5. To verify the installation, try running the script with the help flag:
```bash
python civitai_data_manager.py --help
```

You should see the available command-line options displayed.

## Usage Guide

### Basic Commands

Single File Processing:
```bash
python civitai_data_manager.py --single "path/to/your/model.safetensors"
```

Directory Processing:
```bash
python civitai_data_manager.py --all "path/to/your/models/directory"
```

### Additional Options

- `--output`: Specify output directory (optional)
  ```bash
  python civitai_data_manager.py --single "path/to/model.safetensors" --output "path/to/output"
  ```
  If not provided, the script will prompt you to enter the output directory path.

- `--notimeout`: Disable rate limiting protection (use with caution)
  ```bash
  python civitai_data_manager.py --all "path/to/directory" --notimeout
  ```

- `--images`: Download all preview images for the models
  ```bash
  python civitai_data_manager.py --all "path/to/directory" --images
  ```

- `--noimages`: Disable downloading of preview images
  ```bash
  python civitai_data_manager.py --all "path/to/directory" --noimages
  ```
  If no images-related flag is provided, the script will only download the first preview image from Civitai.

- `--onlynew`: Only process new files that haven't been processed before
  ```bash
  python civitai_data_manager.py --all "path/to/directory" --onlynew
  ```
  The script maintains a list of processed files in the output directory.

- `--onlyhtml`: Generate HTML files from existing data without fetching from Civitai
  ```bash
  python civitai_data_manager.py --all "path/to/directory" --onlyhtml
  ```
  This option skips all API calls and only generates/updates HTML files.

### Recommended Organization

For better organization, run separately for each model category:
```bash
# For checkpoints
python civitai_data_manager.py --all "path/to/checkpoints/sdxl" --output "path/to/backup/checkpoints/sdxl"
python civitai_data_manager.py --all "path/to/checkpoints/flux" --output "path/to/backup/checkpoints/flux"

# For Loras
python civitai_data_manager.py --all "path/to/loras/sdxl" --output "path/to/backup/loras/sdxl"
python civitai_data_manager.py --all "path/to/loras/flux" --output "path/to/backup/loras/flux"
```

### Best Practices

- The first time, run with the options `--all` and `--images`
- Then, run periodically to catch updates with `--onlynew`
- Back up the generated data directory with your models
- Monitor `missing_from_civitai.txt` for manual documentation needs

## Output Structure

### Directory Layout

```
output_directory/
├── model_name/
│   ├── model_name_metadata.json              # SafeTensors metadata
│   ├── model_name_hash.json                  # SHA256 hash
│   ├── model_name_civitai_model_version.json # Model-versions endpoint data from Civitai
│   ├── model_name_civitai_model.json         # Full model data from Civitai
│   ├── model_name_preview_0.jpg              # First preview image
│   ├── model_name_preview_1.jpg              # Additional preview images (if --images used)
│   └── model_name.html                       # Model-specific HTML summary
├── models_manager.html                       # Interactive model browser
├── missing_from_civitai.txt                  # List of models not found on Civitai
└── processed_files.json                      # List of processed files (for --onlynew)
```

### Missing Models Tracking

Format in `missing_from_civitai.txt`:
```
# Files not found on Civitai
# Format: Timestamp | Status Code | Filename
# This file is automatically updated when the script runs

2024-11-06 15:53:56 | Status 404 | model1.safetensors
2024-11-06 15:50:39 | Status 404 | model2.safetensors
```

## Features in Detail

### Rate Limiting Protection
- Default random delay: 6-12 seconds between files
- Disable with `--notimeout` flag (use cautiously)

For example, processing 10 files would take:
- Minimum time: ~54 seconds
- Maximum time: ~108 seconds
- Average time: ~81 seconds

**Note about Rate Limiting:** While Civitai's exact rate limiting policies are not publicly documented, these delays are implemented as a precautionary measure to:
- Be respectful to Civitai's servers
- Avoid getting your requests blocked

If you do not have a lot of files to process, you can disable these delays using the `--notimeout` flag.

### Update Checking
- The script compares Civitai's `updatedAt` timestamp with local data and only processes models with new versions
- Prevents unnecessary API calls and downloads

### Download Images
- The script can download all preview images for your models using the `--images` flag.
- You can disable the images downloading by using the `--noimages` flag.
- By default, only the first preview image will be downloaded.

### HTML Generation
- Individual HTML files for each model showing detailed information
- Global model browser with:
  - Models grouped by type (checkpoint, lora, etc.)
  - Tag-based search functionality
  - Download count and statistics
  - Preview image gallery
  - Links to individual model pages

### Processed Files Tracking
- Maintains a JSON file listing all processed models
- Enables selective processing of new files with `--onlynew`
- Records processing timestamp for each file

## FAQ

### How can you retrieve trigger words for a deleted Lora from Civitai?

If the Lora model has been deleted from Civitai, the script can still generate a `metadata.json` file. Inside this file, look for the JSON properties `"ss_datasets.tag_frequency"` and `"ss_tag_frequency"`, where you'll find the trigger words associated with the model.

### How does this tool compare to other models or Civitai managers?

This tool stands out for its simplicity and lightweight design. It requires no configuration and operates independently of any WebUI (such as A1111, ComfyUI, etc.). With a single command, it scans your directory, gathers information, and generates the necessary files automatically.

## Roadmap

### Medium Priority
- **Add Other Content Type**: Add other content from Civitai (embeddings etc.)
  
### Lower Priority (Future Considerations)
- **File Sorting**: Add option to change the type of sorting in the generated browser.
- **Implement Logging**: Add logging functionality to improve tracking and debugging.
- **Add Progress Tracking**: Integrate a progress bar to display the status of file processing.
- **Ensure Path Validation**: Implement better checks to ensure safe file and directory handling during processing.

## Additional Information

### Contributing
Feel free to open issues or submit pull requests with improvements.

### License
[MIT License](LICENSE.md)

### Acknowledgments
This tool uses the [Civitai API](https://github.com/civitai/civitai/wiki/REST-API-Reference).
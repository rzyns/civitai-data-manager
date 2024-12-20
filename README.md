# Civitai Data Manager

- [Overview](#-overview)
- [Demo](#-demo)
- [Key Benefits](#-key-benefits)
- [Model Compatibility](#-model-compatibility)
- [Getting Started](#-getting-started)
  - [Requirements](#requirements)
  - [Installation](#installation)
- [Usage Guide](#-usage-guide)
  - [Basic Commands](#basic-commands)
  - [Additional Options](#additional-options)
  - [Recommended Organization](#recommended-organization)
  - [Best Practices](#best-practices)
- [Output Structure](#-output-structure)
  - [Directory Layout](#directory-layout)
  - [Missing Models Tracking](#missing-models-tracking)
- [Features in Detail](#-features-in-detail)
  - [Rate Limiting Protection](#rate-limiting-protection)
  - [Update Checking](#update-checking)
  - [HTML Generation](#html-generation)
  - [Processed Files Tracking](#processed-files-tracking)
- [FAQ](#-faq)
- [Roadmap](#-roadmap)
- [Changelog](#-changelog)
- [Additional Information](#-additional-information)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## 📄 Overview

A lightweight tool that fetches and saves metadata, description, tags, hashes, and preview images for SafeTensors model files by querying the Civitai API.

It generates interactive HTML pages for easy collection browsing. The tool is especially useful for maintaining model information (trigger words, usage notes, authors) even after models might be removed from Civitai. By creating a local backup of crucial model data, you can ensure your collection remains well-documented and easily accessible regardless of the models' availability online.

## 🖥️ Demo

![Civitai Data Manager Demo](https://i.imgur.com/jKXxX4S.gif)

<!-- <div style="text-align:center;"><a href="https://win3ry.com/projects/civitai/">Demo</a></div> -->

## ✨ Key Benefits

- **Protect Key Information**: Models may be removed from Civitai, making it crucial to back up their usage instructions for future reference.
- **Save Trigger Words**: Preserve Lora trigger words even if the associated model is no longer available on Civitai.
- **Minimalistic Tool**: A free, straightforward and lightweight solution that doesn't require using an API key.
- **Organize Model Details**: Keep track of model authors, versions, and usage examples for easy reference.
- **Monitor Unavailable Models**: Maintain a record of models you own that have been removed from Civitai.
- **Track Renamed Models**: Find models downloaded from Civitai, even if the file has been renamed.
- **Smart Updates**: Updates only occur for models with new information on Civitai, keeping the process efficient.
- **Generation Example**: Save the prompts and generation details for all the Loras/checkpoints' preview images.

## 🔄 Model Compatibility

Works with all `.safetensors` files available on Civitai:
- Checkpoints
- LoRA, LyCORIS, DoRA
- Control Net models (SafeTensor)
- Embeddings
- ...

## 🚀 Getting Started

### Requirements
- Python 3.10 or higher

### Installation

1. Clone the repository:
```bash
git clone https://github.com/jeremysltn/civitai-data-manager.git
```

2. Navigate to the project directory:
```bash
cd civitai-data-manager
```

3. Install required dependencies (only 1):
```bash
pip install -r requirements.txt
```

4. Make the script executable (Unix-like systems only):
```bash
chmod +x main.py
```

5. To verify the installation, try running the script with the help flag:
```bash
python main.py --help
```

You should see the available command-line options displayed.

## 📖 Usage Guide

You have two ways to use this tool: using a config.json file or options arguments.

### Configuration File

Edit the a `config.json` file in the script directory with your preferred settings. If present, the config file takes precedence over command-line arguments.

Example config for first use (save as `config.json`):
```json
{
    "all": "path/to/models/directory",
    "output": "path/to/output/directory",
    "images": true
}
```

Examples of configuration are located in the `config_examples` directory.

### Basic Usage

- The first time, edit the `config.json` file and simply run:
  ```bash
  python main.py
- To update with the data from newly added models, run periodically to catch updates with the update config (file present in `/config_examples/config.update.json`)

### All Options

All these options can be used in the `config.json` file.

- `--output`: Specify output directory
  ```bash
  python main.py --single "path/to/model.safetensors" --output "path/to/output"
  ```
  If not provided, the script will prompt you to enter the output directory path.

- `--notimeout`: Disable rate limiting protection (use with caution)
  ```bash
  python main.py --all "path/to/model/directory" --notimeout
  ```

- `--images`: Download all preview images for the models
  ```bash
  python main.py --all "path/to/model/directory" --images
  ```
  If this flag is not provided, the script will only download the first preview image.

- `--generateimagejson`: Generate JSON files for all preview images from existing model version data
  ```bash
  python main.py --all "" --output "path/to/directory" --generateimagejson
  ```
  This option is implemented only for data generated before script version 1.3.0

- `--noimages`: Disable downloading of preview images
  ```bash
  python main.py --all "path/to/model/directory" --noimages
  ```

- `--onlynew`: Only process new files that haven't been processed before
  ```bash
  python main.py --all "path/to/model/directory" --onlynew
  ```

- `--skipmissing`: Skip previously missing models when used with `--onlynew`
  ```bash
  python main.py --all "path/to/model/directory" --onlynew --skipmissing
  ```
  If this flag is not provided, the script will always check for previously missing models.

- `--onlyupdate`: Only update metadata for processed models
  ```bash
  python main.py --all "path/to/model/directory" --onlyupdate

- `--onlyhtml`: Generate HTML files from existing data without fetching from Civitai
  ```bash
  python main.py --all "path/to/model/directory" --onlyhtml
  ```
  This option skips all API calls and only generates/updates HTML files.
  
- `--clean`: Remove data for models that no longer exist in source directory
  ```bash
  python main.py --all "path/to/model/directory" --clean

-  `--noconfig`: Ignore config.json and use command line arguments only
  ```bash
  python main.py --all "path/to/model/directory" --images --noconfig
  ```
  This flag is helpful to debug or test configurations without removing the `config.json` file.


### Recommended Organization

For better organization, run separately for each model category:
```bash
# For checkpoints
python main.py --all "path/to/checkpoints/sdxl" --output "path/to/backup/checkpoints/sdxl" --noconfig
python main.py --all "path/to/checkpoints/flux" --output "path/to/backup/checkpoints/flux" --noconfig

# For Loras
python main.py --all "path/to/loras/sdxl" --output "path/to/backup/loras/sdxl" --noconfig
python main.py --all "path/to/loras/flux" --output "path/to/backup/loras/flux" --noconfig
```

### Best Practices

- If you want to update only the Civitai data, use the options `onlyupdate` and `noimages`
- Just in case, always back up the generated data directory with your models
- Monitor `missing_from_civitai.txt` and `duplicate_models.txt` for manual documentation needs

## 🗃️ Output Structure

### Directory Layout

```
output_directory/
├── model_name/
│   ├── model_name_metadata.json              # SafeTensors metadata
│   ├── model_name_hash.json                  # SHA256 hash
│   ├── model_name_civitai_model_version.json # Model-versions endpoint data from Civitai
│   ├── model_name_civitai_model.json         # Full model data from Civitai
│   ├── model_name_preview_0.jpeg             # First preview image
│   ├── model_name_preview_0.json             # Metadata for first preview image
│   ├── model_name_preview_x.jpeg             # Additional preview images (if --images used)
│   ├── model_name_preview_x.json             # Metadata for additional preview images (if --images used)
│   └── model_name.html                       # Model-specific HTML page
├── index.html                                # Model browser
├── missing_from_civitai.txt                  # List of models not found on Civitai
├── duplicate_models.txt                      # List of duplicate models
└── processed_files.json                      # List of processed files
```

### Missing Models Tracking

Format in `missing_from_civitai.txt`:
```
# Files not found on Civitai
# Format: Timestamp | Status Code | Filename
# This file is automatically updated when the script runs
# A file is removed from this list when it becomes available again

2024-11-06 15:53:56 | Status 404 | model1.safetensors
2024-11-06 15:50:39 | Status 404 | model2.safetensors
```

### Duplicate Models Tracking

Format in `duplicate_models.txt`:
```
# Duplicate models found in input directory
# Format: Hash | Kept Model | Removed Duplicates
# This file is automatically updated when running --clean

Hash: <hash>
Kept: <path>\model.safetensors
Removed:
  - <path>\model-2.safetensors
```

## 🔍 Features in Detail

### Rate Limiting Protection
- Default: random delay between 3-6 seconds after each model and 1 second between each picture
- Disable with `--notimeout` flag (use cautiously)

For example, processing 10 models (with 10 pictures each) would take:
- Minimum time: ~127 seconds
- Maximum time: ~154 seconds
- Average time: ~140.5 seconds

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
- Individual HTML files for each model showing detailed information and image gallery with generation details
- Global model browser with:
  - Models grouped by type (checkpoint, lora, etc.)
  - Search functionality (tag, filename, model name)
  - By default, models are sorted by Download count
  - Links to individual model and direct download pages

### Processed Files Tracking
- Maintains a JSON file listing all processed models
- Enables selective processing of new files with `--onlynew`
- Records processing timestamp for each file

## ❓ FAQ

### How can you retrieve trigger words for a deleted Lora from Civitai?

If the Lora model has been deleted from Civitai, the script can still generate a `metadata.json` file. Inside this file, look for the JSON properties `"ss_datasets.tag_frequency"` and `"ss_tag_frequency"`, where you'll find the tags associated with the model. It is not certain that these properties are present. In the future, consider using this script regularly to archive all useful information.

### How does this tool compare to other models or Civitai managers?

This tool stands out for its simplicity and lightweight design. It requires no configuration and operates independently of any WebUI (such as A1111, ComfyUI, etc.). With a single command, it scans your models directory, gathers informations on Civitai, and generates an interactive model browser (`index.html`).

## 🛣️ Roadmap

### Features
- **🔥 Manual model page**: Add a way for users to add manually (via json file and directory scan) - useful if a model was never available on Civitai but downloaded elsewhere
- **File Sorting**: Add option to select the default type of sorting in the generated browser (in the future config file).
- **Filters**: Add option to filter models by Author or Base Model.
- **Dark Mode**: Integrate dark mode in the templates.

### Fixes
- **Special Model Names**: Fix the broken link when model's name has special characters (like `[FLUX.1 [dev] - LoRa] [Style] 'True Real Photography' [SPECTRUM #0001]`)

### Misc.
- **GitHub**: Update GitHub demo and video preview (the current ones are from version 1.1)
- **Implement Logging**: Add better logging functionality to improve tracking and debugging.
- **Add Progress Tracking**: Integrate a progress bar to display the status of file processing.

## 📜 Changelog

- **1.4.3** - fix: Path handling in main function (fixed TypeError when processing command line arguments)
- **1.4.2** - feat: Add --noconfig flag to override config file
- **1.4.1** - fix: Fixed event listener persistence for arrow key navigation between images
- **1.4.0** - 🔥 feat: add JSON configuration file support

- **1.3.6** - feat: Add keyboard navigation for preview images
- **1.3.5** - refactor: Decreasing the default delay between models (from 6-12 to 3-6 seconds)
- **1.3.4** - fix: Improve preview image metadata handling
- **1.3.3** - refactor: Increase model's thumbnail size in the model browser
- **1.3.2** - fix: Handle duplicate file message in clean operation
- **1.3.1** - fix: The scale effect in the model's gallery now affects videos
- **1.3.0** - 🔥 feat: Enhance image modal with detailed metadata display (seed, prompt used etc.)

- **1.2.5** - 🔥 feat: Enhance model browser search functionality
- **1.2.4** - feat: Enhance --clean to detect and handle duplicate models
- **1.2.3** - feat: Add toggleable cover images to model browser
- **1.2.2** - feat: Add --skipmissing option for optimizing model checks
- **1.2.1** - fix: Prevent missing models from appearing in multiple sections
- **1.2.0** - feat: Add video preview support for model galleries

## 📘 Additional Information

### Contributing
Feel free to open issues or submit pull requests with improvements.

### License
[MIT License](LICENSE.md)

### Acknowledgments
In accordance with Civitai's Terms of Service, this tool adheres to the restriction of not accessing, searching, or utilizing any part of the service through unauthorized engines, software, or tools. It only uses the search agents provided by Civitai through their official open [API](https://github.com/civitai/civitai/wiki/REST-API-Reference), ensuring full compliance with the terms.
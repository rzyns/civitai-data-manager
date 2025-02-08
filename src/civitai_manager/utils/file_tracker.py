from pathlib import Path
from datetime import datetime
from typing import Self, TypedDict
import pydantic

from civitai_manager.utils.string_utils import AnyPathLike, pathlike_or_path_to_path
from file_types import ProcessedFilesTA

type ProcessedFileEntry = str

class ProcessedFiles(TypedDict):
    files: list[ProcessedFileEntry]
    last_update: datetime | None
    # Add any other fields you need

class ProcessedFilesManager:
    output_dir: Path
    processed_file: Path
    processed_files: ProcessedFiles

    def __init__(self: Self, output_dir: AnyPathLike):
        self.output_dir = pathlike_or_path_to_path(output_dir)

        self.processed_file = self.output_dir / 'processed_files.json'
        self.processed_files = self._load_processed_files()

    def _load_processed_files(self: Self):
        """Load the list of processed files from JSON"""
        if self.processed_file.exists():
            with open(self.processed_file, 'r') as f:
                return pydantic.TypeAdapter(ProcessedFiles).validate_json(f.read())
        return ProcessedFiles(files=[], last_update=None)

    def save_processed_files(self):
        """Save the current list of processed files"""
        with open(self.processed_file, 'w') as f:
            self.processed_files['last_update'] = datetime.now()
            _ = f.buffer.write(ProcessedFilesTA.dump_json(self.processed_files))

    def is_file_processed(self, file_path: AnyPathLike):
        """Check if a file has been processed before"""
        return str(file_path) in self.processed_files['files']

    def add_processed_file(self, file_path: AnyPathLike):
        """Add a file to the processed list"""
        if str(file_path) not in self.processed_files['files']:
            self.processed_files['files'].append(pathlike_or_path_to_path(file_path).absolute().as_posix())

    def get_new_files(self, directory_path: Path):
        """Get list of new safetensors files that haven't been processed"""
        all_files = list(Path(directory_path).glob('**/*.safetensors'))
        return [Path(f) for f in all_files if not self.is_file_processed(f)]
    
    def update_timestamp(self):
        """Update the last_update timestamp without modifying the files list"""
        self.processed_files['last_update'] = datetime.now()
        self.save_processed_files()

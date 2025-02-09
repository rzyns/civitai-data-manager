from collections.abc import Iterable
from datetime import datetime
from enum import StrEnum
from functools import cached_property
from pathlib import Path
from typing import TypedDict

import pydantic

from civitai import Model
from civitai_manager.utils.string_utils import sanitize_filename


MISSING_FILES_NAME = "missing_from_civitai.txt"

class HashType(StrEnum):
    SHA256 = "SHA256"


HashTypeTA = pydantic.TypeAdapter(HashType)


class HashData(TypedDict):
    model_dir: Path
    safetensors_file: Path
    processed_time: datetime


HashDataTA = pydantic.TypeAdapter(HashData)

class ModelPaths(pydantic.BaseModel):
    safetensors: pydantic.FilePath
    output_dir: Path
    base_dir: Path
    info: Path
    version: Path
    hash: Path
    html: Path

    def as_dict(self) -> dict[str, Path]:
        return {
            "safetensors": self.safetensors,
            "output_dir": self.output_dir,
            "base_dir": self.base_dir,
            "info": self.info,
            "version": self.version,
            "hash": self.hash,
            "html": self.html,
        }

INFO_SUFFIX = "_civitai_model.json"
MODEL_VERSION_SUFFIX = "_civitai_model_version.json"
HASH_SUFFIX = "_hash.json"
HTML_SUFFIX = ".html"

class ModelData(pydantic.BaseModel):
    base_dir: pydantic.DirectoryPath
    safetensors: pydantic.FilePath

    @cached_property
    def sanitized_name(self) -> str:
        return sanitize_filename(self.safetensors.stem)

    @cached_property
    def model(self) -> Model:
        return Model.model_validate_json(self.paths.info.read_text())

    # model: Model

    @cached_property
    def paths(self) -> ModelPaths:
        output_dir = self.base_dir / Path(self.sanitized_name)
        p = ModelPaths(
            base_dir=self.base_dir,
            output_dir=output_dir,
            info=output_dir / Path(f"{self.sanitized_name}{INFO_SUFFIX}"),
            version=output_dir / Path(f"{self.sanitized_name}{MODEL_VERSION_SUFFIX}"),
            hash=output_dir / Path(f"{self.sanitized_name}{HASH_SUFFIX}"),
            safetensors=self.safetensors,
            html=output_dir / Path(f"{self.sanitized_name}{HTML_SUFFIX}"),
        )

        return p

    @cached_property
    def required_paths(self) -> Iterable[Path]:
        return [p for p in filter(lambda p: p.stem.endswith(".json"), self.paths.as_dict().values())]

from datetime import datetime
from typing import NotRequired, TypedDict
import pydantic

from data import HashType
# {'files': [], 'last_update': datetime.datetime(2025, 2, 6, 10, 27, 42, 743594)}


class StoredFile[T](pydantic.BaseModel):
    data: T
    createdAt: pydantic.AwareDatetime
    updatedAt: pydantic.AwareDatetime

class CivitaiVersionFile(TypedDict):
    version: NotRequired[str]
    processed_files: NotRequired[list[str]]
    last_processed_time: NotRequired[str]


CivitaiVersionFileTA = pydantic.TypeAdapter(CivitaiVersionFile)


class HashFileData(TypedDict):
    hash_type: HashType
    hash_value: str
    filename: str
    timestamp: datetime


HashFileDataTA = pydantic.TypeAdapter(HashFileData)


class ProcessedFiles(TypedDict):
    files: list[str]
    last_update: datetime | None

ProcessedFilesTA = pydantic.TypeAdapter(ProcessedFiles)

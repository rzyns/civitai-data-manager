from enum import Enum
from typing import Any, TypedDict
import pydantic
from pydantic_core import CoreSchema, core_schema

type Whatever = Any


class Creator(pydantic.BaseModel):
    username: str
    image: str | None


class Stats(pydantic.BaseModel):
    downloadCount: int
    favoriteCount: int
    commentCount: int
    ratingCount: int
    rating: float


class Fp(Enum):
    Fp16 = "fp16"
    Fp32 = "fp32"


class Size(Enum):
    Full = "full"
    Pruned = "pruned"


class Format(Enum):
    SafeTensor = "SafeTensor"
    PickleTensor = "PickleTensor"
    Other = "Other"


class ModelVersionFileMetadata(pydantic.BaseModel):
    fp: Fp | None = pydantic.Field(default=None)
    size: Size | None = pydantic.Field(default=None)
    format: Format | None = pydantic.Field(default=None)


class ModelVersionFile(pydantic.BaseModel):
    name: str
    sizeKB: float
    pickleScanResult: str
    virusScanResult: str
    scannedAt: str | None = pydantic.Field(default=None)
    primary: bool | None = pydantic.Field(default=None)
    metadata: ModelVersionFileMetadata | None = pydantic.Field(default=None)
    downloadUrl: str


class ModelVersionImage(pydantic.BaseModel):
    url: str
    nsfw: bool = pydantic.Field(default=False)
    width: int
    height: int
    hash: str
    meta: dict[Whatever, Whatever] | None = pydantic.Field(default=None)
    type: str | None = pydantic.Field(default=None)


class ModelVersionStats(pydantic.BaseModel):
    downloadCount: int
    ratingCount: int
    rating: float
    thumbsUpCount: int = pydantic.Field(default=0)
    thumbsDownCount: int = pydantic.Field(default=0)
    favoriteCount: int = pydantic.Field(default=0)
    commentCount: int = pydantic.Field(default=0)
    tippedAmountCount: int | float = pydantic.Field(default=0)


class ModelId(pydantic.NonNegativeInt):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: int, handler: pydantic.GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(pydantic.NonNegativeInt))

class ModelVersionId(pydantic.NonNegativeInt):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: int, handler: pydantic.GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(pydantic.NonNegativeInt))

class ModelVersion(pydantic.BaseModel):
    id: ModelVersionId
    name: str
    description: str | None = pydantic.Field(default=None)
    trainedWords: list[str] | None = pydantic.Field(default=None)
    files: list[ModelVersionFile]
    images: list[ModelVersionImage]
    stats: ModelVersionStats

    baseModel: str

    createdAt: str
    updatedAt: pydantic.AwareDatetime | None = pydantic.Field(default=None)


class Metadata(pydantic.BaseModel):
    totalItems: str
    currentPage: str
    pageSize: str
    totalPages: str
    nextPage: str
    prevPage: str


class Tag(pydantic.BaseModel):
    name: str


class Mode(Enum):
    Archived = "Archived"
    TakenDown = "TakenDown"


class Model(pydantic.BaseModel):
    # Response Fields
    # Name	Type	Description
    # id	number	The identifier for the model
    # name	string	The name of the model
    # description	string	The description of the model (HTML)
    # type	enum (Checkpoint, TextualInversion, Hypernetwork, AestheticGradient, LORA, Controlnet, Poses)	The model type
    # nsfw	boolean	Whether the model is NSFW or not
    # tags	string[]	The tags associated with the model
    # mode	enum (Archived, TakenDown) | null	The mode in which the model is currently on. If Archived, files field will be empty. If TakenDown, images field will be empty
    # creator.username	string	The name of the creator
    # creator.image	string | null	The url of the creators avatar
    # stats.downloadCount	number	The number of downloads the model has
    # stats.favoriteCount	number	The number of favorites the model has
    # stats.commentCount	number	The number of comments the model has
    # stats.ratingCount	number	The number of ratings the model has
    # stats.rating	number	The average rating of the model
    # modelVersions.id	number	The identifier for the model version
    # modelVersions.name	string	The name of the model version
    # modelVersions.description	string	The description of the model version (usually a changelog)
    # modelVersions.createdAt	Date	The date in which the version was created
    # modelVersions.downloadUrl	string	The download url to get the model file for this specific version
    # modelVersions.trainedWords	string[]	The words used to trigger the model
    # modelVersions.files.sizeKb	number	The size of the model file
    # modelVersions.files.pickleScanResult	string	Status of the pickle scan ('Pending', 'Success', 'Danger', 'Error')
    # modelVersions.files.virusScanResult	string	Status of the virus scan ('Pending', 'Success', 'Danger', 'Error')
    # modelVersions.files.scannedAt	Date | null	The date in which the file was scanned
    # modelVersions.files.primary	boolean | undefined	If the file is the primary file for the model version
    # modelVersions.files.metadata.fp	enum (fp16, fp32) | undefined	The specified floating point for the file
    # modelVersions.files.metadata.size	enum (full, pruned) | undefined	The specified model size for the file
    # modelVersions.files.metadata.format	enum (SafeTensor, PickleTensor, Other) | undefined	The specified model format for the file
    # modelVersions.images.id	string	The id for the image
    # modelVersions.images.url	string	The url for the image
    # modelVersions.images.nsfw	string	Whether or not the image is NSFW (note: if the model is NSFW, treat all images on the model as NSFW)
    # modelVersions.images.width	number	The original width of the image
    # modelVersions.images.height	number	The original height of the image
    # modelVersions.images.hash	string	The blurhash of the image
    # modelVersions.images.meta	object | null	The generation params of the image
    # modelVersions.stats.downloadCount	number	The number of downloads the model has
    # modelVersions.stats.ratingCount	number	The number of ratings the model has
    # modelVersions.stats.rating	number	The average rating of the model
    # metadata.totalItems	string	The total number of items available
    # metadata.currentPage	string	The the current page you are at
    # metadata.pageSize	string	The the size of the batch
    # metadata.totalPages	string	The total number of pages
    # metadata.nextPage	string	The url to get the next batch of items
    # metadata.prevPage	string	The url to get the previous batch of items
    id: ModelId
    name: str
    description: str
    type: str
    nsfw: bool
    tags: list[Tag | str]
    mode: Mode | None = pydantic.Field(default=None)
    creator: Creator
    stats: Stats
    metadata: Metadata | None = pydantic.Field(default=None)

    allowCommercialUse: list[str] | None = pydantic.Field(default=None)

class ModelResponseData(Model):
    modelVersions: list[ModelVersion]

class ModelVersionResponseData(ModelVersion):
    modelId: ModelId

class SafeTensorsHeader(TypedDict):
    __metadata__: dict[str, pydantic.JsonValue]


SafetensorsHeaderTA = pydantic.TypeAdapter(SafeTensorsHeader)

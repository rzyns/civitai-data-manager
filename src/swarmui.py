from enum import StrEnum
import json
import requests
import pydantic

class Session(pydantic.BaseModel):
    session_id: str
    user_id: str
    output_append_user: bool
    version: str
    server_id: str
    permissions: list[str] = pydantic.Field(default_factory=list)

class ModelData(pydantic.BaseModel):
    name: str
    title: str | None = pydantic.Field(default=None)
    author: str | None = pydantic.Field(default=None)
    description: str | None = pydantic.Field(default=None)
    preview_image: str | None = pydantic.Field(default=None)
    loaded: bool
    architecture: str | None = pydantic.Field(default=None)
    cls: str | None = pydantic.Field(default=None)
    compat_class: str | None = pydantic.Field(default=None)
    resolution: str
    standard_width: int | float
    standard_height: int | float
    license: str | None = pydantic.Field(default=None)
    date: str
    prediction_type: str | None = pydantic.Field(default=None)
    usage_hint: str | None = pydantic.Field(default=None)
    trigger_phrase: str | None = pydantic.Field(default=None)
    merged_from: str | None = pydantic.Field(default=None)
    tags: list[str] | None = pydantic.Field(default=None)
    is_supported_model_format: bool
    is_negative_embedding: bool
    local: bool
    time_created: int
    time_modified: int
    hash: str | None = pydantic.Field(default=None)
    hash_sha256: str | None = pydantic.Field(default=None)
    special_format: str | None = pydantic.Field(default=None)

class ListModelsData(pydantic.BaseModel):
    folders: list[str]
    files: list[ModelData]

class ModelSubtype(StrEnum):
    LORA = "LoRA"

class ListModelsOptions(pydantic.BaseModel):
    depth: int = pydantic.Field()
    path: str = pydantic.Field()
    subtype: ModelSubtype = pydantic.Field()

class DescribeModelResponse(pydantic.BaseModel):
    model: ModelData

def get_new_session():
    result = requests.post(
        "http://localhost:7801/API/GetNewSession",
        headers={"Content-Type": "application/json"},
        data="{}"
    )

    return Session.model_validate(result.json())

def list_models(session_id_or_session: str | Session, opts: ListModelsOptions | None = None):
    if isinstance(session_id_or_session, Session):
        session_id = session_id_or_session.session_id
    else:
        session_id = session_id_or_session

    opts = opts or ListModelsOptions(
        subtype=ModelSubtype.LORA,
        depth=1,
        path="/",
    )


    data = {"session_id": session_id, **opts.model_dump(exclude_unset=True)}

    result = requests.post(
        "http://localhost:7801/API/ListModels",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data),
    )

    try:
        return ListModelsData.model_validate(result.json())
    except requests.exceptions.JSONDecodeError as e:
        raise Exception(f"Error decoding json for {opts}") from e
        return result.text

def describe_model(session_id_or_session: str | Session, subtype: ModelSubtype, model_name: str):
    if isinstance(session_id_or_session, Session):
        session_id = session_id_or_session.session_id
    else:
        session_id = session_id_or_session

    data = {"session_id": session_id, "modelName": model_name, "subtype": subtype}
    result = requests.post(
        "http://localhost:7801/API/DescribeModel",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data),
    )

    return DescribeModelResponse.model_validate(result.json())


if __name__ == "__main__":
    session = Session.model_validate(get_new_session())
    models = list_models(session)
    if models.files:
        m = describe_model(session, ModelSubtype.LORA, models.files[0].name)
        print(m)

from pydantic import TypeAdapter
import civitai
import json

def test_ModelResponseData():
    with open("test_data/ModelResponseData.json", "r") as f:
        data: civitai.ModelResponseData = json.loads(f.read())
        _ = TypeAdapter(civitai.Creator).validate_python(data.get("creator"))
        _ = TypeAdapter(list[civitai.Tag]).validate_python(data.get("tags"))
        _ = TypeAdapter(civitai.Stats).validate_python(data.get("stats"))

        _ = TypeAdapter(civitai.ModelVersion).validate_python(data.get("modelVersions")[0])

        _ = TypeAdapter(civitai.ModelResponseData).validate_python(data)

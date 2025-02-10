from pydantic import TypeAdapter
import civitai
import json

def test_ModelResponseData():
    with open("test_data/ModelResponseData.json", "r") as f:
        data = json.loads(f.read())
        _ = civitai.Creator.model_validate_json(json.dumps(data["creator"]))
        _ = TypeAdapter(list[civitai.Tag]).validate_json(json.dumps(data["tags"]))
        _ = civitai.Stats.model_validate_json(json.dumps(data["stats"]))

        _ = civitai.ModelVersion.model_validate_json(json.dumps(data["modelVersions"][0]))

        _ = civitai.ModelResponseData.model_validate_json(json.dumps(data))

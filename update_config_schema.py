import json
from pathlib import Path
from civitai_manager.utils.config import Config

schema = Config.model_json_schema(mode="validation")
schema["additionalProperties"] = False
schema["properties"]["$schema"] = {
    "type": "string",
}

_ = Path("./config.schema.json").write_text(json.dumps(schema, indent=4))

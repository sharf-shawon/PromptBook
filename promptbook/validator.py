import json
import yaml
import jsonschema
from jsonschema import validate
import os

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "prompt-schema.json")

def load_schema():
    """Load the JSON schema for prompt validation."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def validate_prompt_file(prompt_file):
    """Validate a YAML prompt file against the schema."""
    try:
        with open(prompt_file, "r", encoding="utf-8") as file:
            prompt_data = yaml.safe_load(file)

        schema = load_schema()
        validate(instance=prompt_data, schema=schema)

        print(f"✅ Validation successful: {prompt_file}")
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"❌ Validation failed: {e.message}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

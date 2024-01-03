import os
from jsonschema import validate, ValidationError
from utils.json_reader import JsonReader


class JsonValidator:

    @staticmethod
    def validate_schema(json_content, schema_type):
        schema_file = f"{schema_type}_schema.json"
        schema_path = os.path.join(os.getenv("SCHEMAS_DIRECTORY"), schema_file)

        read_result, schema_content = JsonReader.read_json_file(schema_path)
        if not read_result:
            print(f"[ERROR] Impossible validate schema {schema_type}")
            return

        try:
            validate(json_content, schema_content)
        except ValidationError:
            raise Exception(f"[ERROR] Impossible validate JSON content against schema {schema_type}")

import os

from jsonschema import validate, ValidationError
from utils.json_reader import JsonReader
class JsonValidator:

    @staticmethod
    def validate_schemas():
        file_list = os.listdir(os.getenv("SCHEMAS_DIRECTORY"))

        for file in file_list:
            actual_file_path = "./json/" + file.split("-schema")[0] + ".json"
            schema_path = os.getenv("SCHEMAS_DIRECTORY") + file

            read_result , file_content = JsonReader.read_json_file(actual_file_path)
            if not read_result:
                print("[ERROR] Impossible validate schema")
            read_result , schema_content = JsonReader.read_json_file(schema_path)
            if not read_result:
                print("[ERROR] Impossible validate schema")

            try:
                validate(file_content , schema_content)
            except ValidationError:
                raise ValidationError(f"[ERROR] Impossible validate file {actual_file_path}")

import sys
import requests
from dotenv import load_dotenv
from model.json_validator import JsonValidator
from utils.json_reader import JsonReader
from jsonschema import ValidationError

load_dotenv()

CONFIGURATION_FILE_PATH = "./json/orchestrator-configuration.json"

if __name__ == "__main__":
    try:
        JsonValidator.validate_schemas()
    except ValidationError as e:
        print("[ERROR] Impossible validate json configuration file : " , str(e))
        sys.exit(1)

    res, file_content = JsonReader.read_json_file(CONFIGURATION_FILE_PATH)
    if res is False:
        print("[ERROR] Impossible to read json file\nShutdown")
        sys.exit(1)

    for key in file_content.keys():
        print(f"[INFO] Sending start message to {key}")
        uri = f"http://{file_content[key]['ip']}:{str(file_content[key]['port'])}/start"
        try:
            start_res = requests.get(uri, timeout= 3)
            if start_res.status_code != 200:
                print(f"[ERROR] Not received 200 from {key}: ")
                sys.exit(1)
        except Exception as e:
            print(f"[ERROR] Impossible to send start request to {key}: " , str(e))
            sys.exit(1)

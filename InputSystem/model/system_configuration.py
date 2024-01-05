import os
from utils.json_reader import JsonReader

class SystemConfiguration:

    def __init__(self):
        read_result, file_content = JsonReader.read_json_file(os.getenv("CONFIG_FILE_PATH"))
        if not read_result:
            return
        self.situation = file_content["situation"]
        self.probability = file_content["probability-of-error"]
        self.interval = file_content["interval"]

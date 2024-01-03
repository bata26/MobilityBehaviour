import os
from utils.json_reader import JsonReader
from model.json_validator import JsonValidator


class MessageConfiguration:

    def __init__(self):
        read_result, file_content = JsonReader.read_json_file(os.getenv("MESSAGE_CONFIG_FILE_PATH"))
        if not read_result:
            return
        JsonValidator.validate_schema(file_content, "message_configuration")
        self.host_src_ip = file_content["src"]["ip"]
        self.host_src_port = file_content["src"]["port"]

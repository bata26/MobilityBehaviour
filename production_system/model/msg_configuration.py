import os

from utils.json_reader import JsonReader

class MessageConfiguration:

    def __init__(self):
        print("STO PER LEGGERE IL FILE : " , os.getenv("MESSAGE_CONFIG_FILE_PATH"))
        read_result, file_content = JsonReader.read_json_file(os.getenv("MESSAGE_CONFIG_FILE_PATH"))
        if not read_result:
            return
        self.host_src_ip = file_content["src"]["ip"]
        self.host_src_port = file_content["src"]["port"]
        self.evaluation_system_ip = file_content["evaluation-system"]["ip"]
        self.evaluation_system_port = file_content["evaluation-system"]["port"]
        self.client_system_ip = file_content["client-system"]["ip"]
        self.client_system_port = file_content["client-system"]["port"]
        self.messaging_system_ip = file_content["messaging-system"]["ip"]
        self.messaging_system_port = file_content["messaging-system"]["port"]

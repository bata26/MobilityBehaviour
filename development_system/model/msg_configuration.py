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
        self.host_dest_ip = file_content["dest"]["ip"]
        self.host_dest_port = file_content["dest"]["port"]

import os

from utils.json_reader import JsonReader

class SystemConfiguration:

    def __init__(self):
        read_result, file_content = JsonReader.read_json_file(os.getenv("CONFIG_FILE_PATH"))
        if not read_result:
            return
        self.evaluation_phase = file_content["evaluation-phase"]
        self.classifier_deployed = file_content["classifier-deployed"]
    
    def update_classifier(self , value):
        self.classifier_deployed = value
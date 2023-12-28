import os

from utils.json_reader import JsonReader

class SystemConfiguration:

    def __init__(self):
        print("CONFIGGG STO PER LEGGERE IL FILE : " , os.getenv("CONFIG_FILE_PATH"))
        read_result, file_content = JsonReader.read_json_file(os.getenv("CONFIG_FILE_PATH"))
        if not read_result:
            return
        #self.endpoint_ip = file_content["endpoint-ip"]
        #self.endpoint_port = file_content["endpoint-port"]
        self.starting_mode = file_content["starting-mode"]
        self.default_iterations_number = file_content["default-iterations-number"]
        self.validation_threshold = file_content["validation-threshold"]
        self.test_threshold = file_content["test-threshold"]
        self.hidden_neurons = file_content["hidden-neurons"]
        self.ongoing_validation = file_content["ongoing-validation"]
        self.flow = {
            "learning_plot_result" : file_content["flow"]["learning-plot-result"]
        }
    def get_default_iterations_number(self):
        return self.default_iterations_number

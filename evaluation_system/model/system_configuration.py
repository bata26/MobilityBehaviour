import os
from utils.json_reader import JsonReader


class SystemConfiguration:

    def __init__(self, path):
        if path is None:
            read_result, file_content = JsonReader.read_json_file(os.getenv("CONFIG_FILE_PATH"))
            if not read_result:
                return

            self.db_name = file_content["db_name"]
            self.sufficient_labels = file_content["sufficient_labels"]
            self.max_number_of_tolerated_errors = file_content["max_number_of_tolerated_errors"]
            self.max_number_of_consecutive_tolerated_errors = file_content["max_number_of_consecutive_tolerated_errors"]
        else:
            read_result, file_content = JsonReader.read_json_file(path)
            if not read_result:
                return

            self.db_name = file_content["db_name"]
            self.sufficient_labels = file_content["sufficient_labels"]
            self.max_number_of_tolerated_errors = file_content["max_number_of_tolerated_errors"]
            self.max_number_of_consecutive_tolerated_errors = file_content["max_number_of_consecutive_tolerated_errors"]

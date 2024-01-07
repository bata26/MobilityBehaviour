import sys
import json
import logging
from utility.json_handler import JsonHandler

class PreparationSystemConfiguration:
    """
    Class responsible for retrieving and validating the configuration parameters
    set by the system administrator. It offers the parameters as public attributes.
    """
    def __init__(self, json_configuration_path: str, json_schema_path: str) -> None:
        """
        ``Configuration`` constructor
        :param json_configuration_path: path to the configuration file
        :param json_schema_path:  path to the json schema of the configuration file
        """
        json_handler = JsonHandler()

        # Open the configuration file
        with open(json_configuration_path, "r", encoding="UTF-8") as file:
            # Load JSON configuration
            json_conf = json.load(file)
            # Validate configuration
            if not json_handler.validate_json_data_file(json_conf, json_schema_path):
                logging.error("Impossible to load the preparation system "
                              "configuration: JSON file is not valid")
                raise ValueError("Preparation System configuration failed")
            # Add JSON attributes to current object
            self.production_system_ip = json_conf['production_system_ip']
            self.segregation_system_ip = json_conf['segregation_system_ip']
            self.production_system_port = json_conf['production_system_port']
            self.segregation_system_port = json_conf['segregation_system_port']
            self.operative_mode = json_conf['operative_mode']
            self.max_value = int(json_conf['max_value'])
            self.min_value = int(json_conf['min_value'])
            self.features = json_conf['features']

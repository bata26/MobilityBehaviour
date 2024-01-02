import json
import logging
from utility.json_handler import validate_json_data_file


class IngestionSystemConfiguration:
    """
    Class responsible for retrieving and validating the configuration parameters
    set by the system administrator. It offers the parameters as public attributes.
    """
    
    def __init__(self, json_configuration_path: str, json_schema_path: str):
        """
        ``Configuration`` constructor
        :param json_configuration_path: path to the configuration file
        :param json_schema_path:  path to the json schema of the configuration file
        """
        # Open the configuration file
        with open(json_configuration_path, "r", encoding="UTF-8") as file:
            # Load JSON configuration
            json_conf = json.load(file)
            # Validate configuration
            if not validate_json_data_file(json_conf, json_schema_path):
                logging.error("Impossible to load the ingestion system "
                              "configuration: JSON file is not valid")
                raise ValueError("Ingestion System configuration failed")
            
            # Add JSON attributes to current object
            self.production_system_ip = json_conf['preparation_system_ip']
            self.segregation_system_ip = json_conf['evaluation_system_ip']
            self.production_system_port = json_conf['preparation_system_port']
            self.segregation_system_port = json_conf['evaluation_system_port']
            self.features = json_conf['features']
            self.operative_mode = bool(json_conf['operative_mode'])
            self.max_value = json_conf['max_value']
            self.min_value = json_conf['min_value']

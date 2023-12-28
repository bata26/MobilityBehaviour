import json
import logging
import os
import utility
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
        with open(os.path.join(utility.data_folder, json_configuration_path),
                  "r", encoding="UTF-8") as file:
            # Load JSON configuration
            json_conf = json.load(file)
            # Validate configuration
            if not validate_json_data_file(json_conf, json_schema_path):
                logging.error("Impossible to load the ingestion system "
                              "configuration: JSON file is not valid")
                raise ValueError("Ingestion System configuration failed")
            
            # Add JSON attributes to current object
            #self.ip_address = json_conf['ip_address']
            #self.port = int(json_conf['port'])
            self.database_path = json_conf['database_path']
            self.preparation_system_ip = json_conf['preparation_system_ip']
            self.evaluation_system_ip = json_conf['evaluation_system_ip']
            self.preparation_system_port = json_conf['preparation_system_port']
            self.evaluation_system_port = json_conf['evaluation_system_port']
            self.missing_samples_threshold = int(json_conf['missing_samples_threshold'])
            self.execution_window= int(json_conf['production_window'])
            self.evaluation_window = int(json_conf['evaluation_window'])
            self.operative_mode = bool(json_conf['operative_mode'])

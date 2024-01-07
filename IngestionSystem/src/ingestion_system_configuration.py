import json
import logging
from utility.json_handler import JsonHandler


class IngestionSystemConfiguration:
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
        with open(json_configuration_path,
                  "r", encoding="UTF-8") as file:
            # Load JSON configuration
            json_conf = json.load(file)
            # Validate configuration
            if not json_handler.validate_json_data_file(json_data=json_conf, \
                                                        schema_path=json_schema_path):
                logging.error("Impossible to load the ingestion system "
                              "configuration: JSON file is not valid")
                raise ValueError("Ingestion System configuration failed")

            # Add JSON attributes to current object
            self.db_name = json_conf['db_name']
            self.preparation_system_ip = json_conf['preparation_system_ip']
            self.evaluation_system_ip = json_conf['evaluation_system_ip']
            self.preparation_system_port = json_conf['preparation_system_port']
            self.evaluation_system_port = json_conf['evaluation_system_port']
            self.missing_samples_threshold = int(json_conf['missing_samples_threshold'])
            self.production_window= int(json_conf['production_window'])
            self.evaluation_window = int(json_conf['evaluation_window'])
            self.operative_mode = json_conf['operative_mode']

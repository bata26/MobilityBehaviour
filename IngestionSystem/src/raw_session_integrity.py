import sys
from jsonschema import ValidationError
from src.ingestion_system_configuration import IngestionSystemConfiguration

CONFIG_PATH = './data/ingestion_system_config.json'
CONFIG_SCHEMA_PATH = './data/ingestion_system_config_schema.json'

'''
Module Name: RawSessionIntegrity
Description: This class acts as a marker for the missing samples.
'''
class RawSessionIntegrity:
    """
    Class that marks the missing samples in a time series
    """
    def __init__(self):
        """
        Initializes the checker for the raw session integrity 
        """
        try:
            self.configuration = IngestionSystemConfiguration(CONFIG_PATH, CONFIG_SCHEMA_PATH)
        except ValidationError:
            sys.exit(1)

    def mark_missing_samples(self, time_series: list) -> bool:
        """
        Detects and marks the missing pressure time series in a Raw Session.
        :param time_series: list of pressure time series (represented as list of integers)
        :param threshold: maximum threshold of missing samples tolerated
        :return: True if the number of missing samples detected meets the requirements. 
        False otherwise.
        """
        missing_samples = 0
        for value in time_series:
            if value is None:
                missing_samples += 1
        return missing_samples <= self.configuration.missing_samples_threshold

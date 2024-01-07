import sys
from jsonschema import ValidationError
from src.preparation_system_configuration import PreparationSystemConfiguration

CONFIG_PATH = './data/preparation_system_config.json'
CONFIG_SCHEMA_PATH = './data/preparation_system_config_schema.json'

'''
Module Name: SessionCleaning
Description: This class corrects the missing samples 
and the outliers.
'''
class SessionCleaning:
    """
    Class that corrects through interpolation the missing samples
    and corrects the outliers through substitution
    """
    def __init__(self) -> None:
        try:
            self.configuration = PreparationSystemConfiguration(CONFIG_PATH, CONFIG_SCHEMA_PATH)
        except ValidationError:
            sys.exit(1)
        self.min_value = self.configuration.min_value
        self.max_value = self.configuration.max_value

    def correct_missing_samples(self, time_series: list) -> bool:
        """
        Checks for missing samples in the list of pressure time series;
        if they are recoverable, the missing samples are corrected.
        :param time_series: List of time_series.
        :return: True if there are no missing samples or the missing ones are recoverable.
        """
        for i, value in enumerate(time_series):
            # If a sample is missing the interpolation is computed
            if value is None:
                print(f'[-] Value nr. { + 1} is missing')
                if 3 <= i <= 1232:
                    self.interpolate_list(time_series, i)
                else:
                    return False
        return True

    @staticmethod
    def interpolate_list(time_series, missing_value) -> None:
        """
        Interpolates the specified value with the adjacent ones in the list.
        :param time_series: List of time series.
        :param missing_value: The value to interpolate.
        :return: None
        """
        # List of adjacent value in the time_series
        lists_to_use = [missing_value - 1, missing_value + 1, missing_value - 2, \
                        missing_value + 2, missing_value - 3, missing_value + 3]

        value = 0
        list_number = 0
        for i in lists_to_use:
            if time_series[i]:
                value += time_series[i]
                list_number += 1
        if list_number != 0:
            time_series[missing_value] = value / list_number

    def correct_outliers(self, time_series: list) -> None:
        """
        Corrects outliers in the data.
        :param time_series: List of time series.
        :return: None
        """
        for i, value in enumerate(time_series):
            if value > self.max_value:
                time_series[i] = self.max_value
            elif value < self.min_value:
                time_series[i] = self.min_value

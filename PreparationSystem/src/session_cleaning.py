import json
import os
from jsonschema import validate, ValidationError
from utility.json_handler import validate_json_file_file


class SessionCleaning:

    def correct_missing_samples(self, time_series: list):
        """
        Checks for missing samples in the list of pressure time series;
        if they are recoverable, the missing samples are corrected.
        :param time_series: List of time_series.
        :return: True if there are no missing samples or the missing ones are recoverable.
        """
        for i in range(len(time_series)):
            # If a sample (a channel) is missing the interpolation is computed
            if not time_series[i]:
                print(f'[-] Value nr. { + 1} is missing')
                if 3 <= i <= 1232:
                    self.interpolate_list(time_series, i)
                else:
                    return False
        return True

    @staticmethod
    def interpolate_list(time_series, missing_value):
        """
        Interpolates the specified value with the adjacent ones in the list.
        :param time_series: List of time series.
        :param missing_value: The value to interpolate.
        :return: None
        """
        # List of adjacent value in the time_series
        lists_to_use = [missing_value - 1, missing_value + 1, missing_value - 2, missing_value + 2, missing_value - 3, missing_value + 3]

        value = 0
        list_number = 0
        for i in lists_to_use:
            if time_series[i]:
                value += time_series[i]
                list_number += 1
        if list_number != 0:
            time_series[missing_value].append(value / list_number)

    @staticmethod
    def correct_outliers(time_series: list, min_value: int, max_value: int):
        """
        Corrects outliers in the data.
        :param headset: List of time series.
        :param min_value: Lower bound.
        :param max_value: Upper bound.
        :return: None
        """
        for value in time_series:
            if value > max_value:
                value = max_value
            elif value < min_value:
                value = min_value

    @staticmethod
    def validate_raw_session(raw_session: dict):
        """
        Validates the received raw session according to the loaded schema.
        :param raw_session: The dict containing the received raw session.
        :return: True if the raw session is valid, False if it is not valid.
        """
        try:

            with open(os.path.join(os.path.abspath('..'), 'data', 'raw_session_schema.json')) as f:
                schema = json.load(f)

            validate(raw_session, schema)
            return True

        except FileNotFoundError:
            print('[-] Failed to open schema file')
            return False

        except ValidationError:
            return False



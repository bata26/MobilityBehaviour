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
    def correct_missing_samples(self, time_series: list):
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
    def interpolate_list(time_series, missing_value):
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

    @staticmethod
    def correct_outliers(time_series: list, min_value: float, max_value: float):
        """
        Corrects outliers in the data.
        :param time_series: List of time series.
        :param min_value: Lower bound.
        :param max_value: Upper bound.
        :return: None
        """
        for i, value in enumerate(time_series):
            if value > max_value:
                time_series[i] = max_value
            elif value < min_value:
                time_series[i] = min_value

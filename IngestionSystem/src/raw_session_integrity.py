'''
Module Name: RawSessionIntegrity
Description: This class acts as a marker for the missing samples.
'''
class RawSessionIntegrity:
    """
    Class that marks the missing samples in a time series
    """
    @staticmethod
    def mark_missing_samples(time_series: list, threshold: int) -> bool:
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

        return missing_samples <= threshold


class RawSessionIntegrity:
    
    @staticmethod
    def mark_missing_samples(time_series: list, threshold: int) -> bool:
        """
        Detects and marks the missing pressure time series in a Raw Session.
        :param time_series: list of pressure time series (represented as list of integers)
        :param threshold: maximum threshold of missing samples tolerated
        :return: True if the number of missing samples detected meets the requirements. False otherwise.
        """

        missing_samples = 0
        for i in range(0, len(time_series)):
            if not time_series[i]:
                missing_samples += 1

        return missing_samples <= threshold

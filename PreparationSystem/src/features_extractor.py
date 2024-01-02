import numpy as np
from scipy.signal import welch
from scipy.integrate import simps


class FeaturesExtractor:
    """
    Class that extracts features and prepares the session to be sent.
    """

    def extract_features(self, features: dict, raw_session: dict, prepared_session: dict, operative_mode: str):
        """
        Extracts the relevant features from the session data.
        :param features: Dictionary of features to extract from pressure time series session data.
        :param raw_session: Raw session data.
        :param prepared_session: Dictionary to store the prepared session to send.
        :param operative_mode: Production or development mode.
        :return: None
        """
        max_pressure, min_pressure, median_pressure, mean_absolute_deviation = self.extract_shoes_sensors_features(raw_session['time_series'], features)
        if operative_mode == 'development':
            self.prepare_session_development(raw_session, prepared_session, max_pressure, min_pressure, median_pressure, mean_absolute_deviation)
        elif operative_mode == 'production':
            self.prepare_session_production(raw_session, prepared_session, max_pressure, min_pressure, median_pressure, mean_absolute_deviation)

    def extract_shoes_sensors_features(self, time_series: list):
        """
        Extracts the relevant features from the preussure time series data of the raw session data.
        :param time_series: List of pressure time series.
        :param features: Dictionary of features to extract from the pressure time series.
        :return: Lists of extracted features.
        """
        max_pressure, min_pressure, median_pressure, mean_absolute_deviation  = None
        
        max_pressure = max(time_series)

        min_pressure = min(time_series)

        median_pressure = np.median(time_series)

        mean_value = np.mean(time_series)
        mean_absolute_deviation = np.mean(np.abs(np.array(time_series) - mean_value))
        
        return max_pressure, min_pressure, median_pressure, mean_absolute_deviation


    @staticmethod
    def prepare_session_development(raw_session: dict, prepared_session: dict, max_pressure: int, min_pressure: int,
                                     median_pressure: int, mean_absolute_deviation: int):
        """
        Prepares the session (development mode).
        :param raw_session: Raw session data.
        :param prepared_session: Dictionary to store the prepared session to be sent.
        :param max_pressure: Max pressure detected.
        :param min_pressure: Min pressure detected.
        :param median_pressure: Median pressure detected.
        :param mean_absolute_deviation: MAD of the detected time series.
        :return: None
        """
        prepared_session['uuid'] = raw_session['uuid']
        prepared_session['features'] = {}
        prepared_session['features']['maximum_pressure_ts'] = max_pressure
        prepared_session['features']['minimum_pressure_ts'] = min_pressure
        prepared_session['features']['median_pressure_ts'] = median_pressure
        prepared_session['features']['mean_absolute_deviation_pressure_ts'] = mean_absolute_deviation
        prepared_session['features']['environment_and_small_scatter'] = raw_session['environment']
        prepared_session['features']['activity_and_small_scatter'] = raw_session['calendar']
        prepared_session['pressure_detected'] = raw_session['pressure_detected']

    @staticmethod
    def prepare_session_production(raw_session: dict, prepared_session: dict, max_pressure: int, min_pressure: int,
                                   median_pressure: int, mean_absolute_deviation: int):
        """
        Prepares the session (production mode).
        :param raw_session: Raw session data.
        :param prepared_session: Dictionary to store the prepared session to be sent.
        :param max_pressure: Max pressure detected.
        :param min_pressure: Min pressure detected.
        :param median_pressure: Median pressure detected.
        :param mean_absolute_deviation: MAD of the detected time series.
        :return: None
        """
        prepared_session['uuid'] = raw_session['uuid']

        environment = raw_session['environment']
        calendar = raw_session['calendar']
        prepared_session['features'] = [max_pressure] + [min_pressure] + [median_pressure] + [mean_absolute_deviation] + [environment] + [calendar]

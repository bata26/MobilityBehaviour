import random
import sys
import numpy as np
from jsonschema import ValidationError
from src.preparation_system_configuration import PreparationSystemConfiguration

CONFIG_PATH = './data/preparation_system_config.json'
CONFIG_SCHEMA_PATH = './data/preparation_system_config_schema.json'

class FeaturesExtractor:
    """
    Class that extracts features and prepares the session to be sent.
    """
    def __init__(self) -> None:
        """
        Initializes a new Features Extractor instance.
        """
        try:
            self.configuration = PreparationSystemConfiguration(CONFIG_PATH, CONFIG_SCHEMA_PATH)
        except ValidationError:
            sys.exit(1)

    def extract_features(self, raw_session: dict, prepared_session: dict):
        """
        Extracts the relevant features from the session data.
        :param raw_session: Raw session data.
        :param prepared_session: Dictionary to store the prepared session to send.
        :return: None
        """
        max_pressure, min_pressure, median_pressure, \
            mean_absolute_deviation, env_and_scatter, act_and_scatter = \
            self.extract_shoes_sensors_features(raw_session, self.configuration.features)
        self.prepare_session(raw_session, prepared_session, max_pressure, min_pressure, \
                        median_pressure, mean_absolute_deviation, env_and_scatter, act_and_scatter)

    def extract_shoes_sensors_features(self, raw_session: list, features: dict):
        """
        Extracts the relevant features from the preussure time series data of the raw session data.
        :param time_series: List of pressure time series.
        :param features: Dictionary of features to extract from the pressure time series.
        :return: Lists of extracted features.
        """

        max_pressure = max(raw_session['time_series'])

        min_pressure = min(raw_session['time_series'])

        median_pressure = np.median(raw_session['time_series'])

        mean_value = np.mean(raw_session['time_series'])
        mean_absolute_deviation = np.mean(np.abs(np.array(raw_session['time_series']) - mean_value))

        operation_env = random.randint(0, 1)
        scattering_env = random.uniform(0, 0.5)
        operation_act = random.randint(0, 1)
        scattering_act = random.uniform(0, 0.5)
        environment_and_small_scatter = None
        activity_and_small_scatter = None

        if operation_env == 0:
            environment_and_small_scatter = features['environment'][raw_session['environment']] + \
                scattering_env
        else:
            environment_and_small_scatter = features['environment'][raw_session['environment']] - \
                scattering_env

        if operation_act == 0:
            activity_and_small_scatter = features['calendar'][raw_session['calendar']] + \
                scattering_act
        else:
            activity_and_small_scatter = features['calendar'][raw_session['calendar']] - \
                scattering_act
        return max_pressure, min_pressure, median_pressure, \
            mean_absolute_deviation, environment_and_small_scatter, activity_and_small_scatter
    
    @staticmethod
    def prepare_session(raw_session: dict, prepared_session: dict, max_pressure: int,
                        min_pressure: int, median_pressure: int, mean_absolute_deviation: int,
                        env_and_scatter: int, act_and_scatter: int):
        """
        Prepares the session (development mode).
        :param raw_session: Raw session data.
        :param prepared_session: Dictionary to store the prepared session to be sent.
        :param max_pressure: Max pressure detected.
        :param min_pressure: Min pressure detected.
        :param median_pressure: Median pressure detected.
        :param mean_absolute_deviation: MAD of the detected time series.
        :param env_and_scatter: environment and small scatter
        :param act_and_scatter: activity and small scatter
        :return: None
        """
        prepared_session['_id'] = raw_session['uuid']
        prepared_session['calendar'] = raw_session['calendar']
        prepared_session['environment'] = raw_session['environment']
        prepared_session['label'] = raw_session['pressure_detected']
        prepared_session['features'] = {}
        prepared_session['features']['maximum_pressure_ts'] = max_pressure
        prepared_session['features']['minimum_pressure_ts'] = min_pressure
        prepared_session['features']['median_pressure_ts'] = median_pressure
        prepared_session['features']['mean_absolute_deviation_pressure_ts'] = mean_absolute_deviation
        prepared_session['features']['environment_and_small_scatter'] = env_and_scatter
        prepared_session['features']['activity_and_small_scatter'] = act_and_scatter

        print(prepared_session)

from datetime import datetime
from threading import Thread
from src.json_io import JsonIO
from src.session_cleaning import SessionCleaning
from src.features_extractor import FeaturesExtractor
from src.preparation_system_configuration import PreparationSystemConfiguration
import logging
from jsonschema import ValidationError

CONFIG_PATH = './data/preparation_system_config.json'
CONFIG_SCHEMA_PATH = './data/preparation_system_config_schema.json'

class PreparationSystem:
    """
    Class that controls the execution of the Preparation System calling all the necessary functions to produce
    the prepared session from the raw one.
    """

    def __init__(self):
        """
        Initializes the PreparationSystem class, validates the configuration and sets the instance variables
        for raw and prepared sessions.
        """
        try:
            self.configuration = PreparationSystemConfiguration(CONFIG_PATH, CONFIG_SCHEMA_PATH)
        except ValidationError:
            logging.error('Error during the Preparation System initialization phase')
            exit(-1)
        
        print(f'[+] The configuration is valid, {self.configuration.operative_mode} mode')
        self.raw_session = None
        self.prepared_session = None

    def run(self):
        """
        Method that runs all the instructions needed for session preparation.
        It continuously listens for new raw sessions, processes them, extracts features,
        prepares the session and sends it to the corresponding endpoint based on the current operating mode.
        :return: None
        """
        # Start the Flask app listener on the port specified
        listener_thread = Thread(target=JsonIO.get_instance().listener, args=('0.0.0.0', 5000), daemon=True)
        listener_thread.start()

        while True:
            # Get received raw session
            self.raw_session = JsonIO.get_instance().get_received_json()
            print('[+] Raw session received')
            print(self.raw_session)
            # Check raw session validity
            if SessionCleaning.validate_raw_session(self.raw_session):
                print('[+] Raw session is valid')
            else:
                print('[-] Raw session is not valid')
                continue

            # Correct missing samples
            if SessionCleaning().correct_missing_samples(self.raw_session['time_series']):
                print('[+] Pressure time series ok')
            else:
                print('[-] Missing samples are unrecoverable, raw session discarded')
                continue
            
            # Correct outliers
            SessionCleaning.correct_outliers(self.raw_session['time_series'],
                                             self.configuration.min_value,
                                             self.configuration.max_value)

            # Extract features and prepare session
            self.prepared_session = {}
            FeaturesExtractor().extract_features \
                (self.raw_session, self.prepared_session, self.configuration.features)
            print('[+] Features extracted and session prepared')

            # Send prepared session to the endpoint corresponding to the current operating mode
            if self.configuration.operative_mode == 'development':
                if JsonIO.get_instance().send(self.configuration.segregation_system_ip,
                                              self.configuration.segregation_system_port,
                                              self.prepared_session):
                    print(f'[+] Prepared session sent at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

            elif self.configuration.operative_mode == 'production':
                if JsonIO.get_instance().send(self.configuration.production_system_ip,
                                              self.configuration.production_system_port,
                                              self.prepared_session):
                    print(f'[+] Prepared session sent at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                    exit(0)


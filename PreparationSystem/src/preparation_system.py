import sys
import time
from datetime import datetime
from threading import Thread
import logging
from jsonschema import ValidationError
from src.json_io import JsonIO
from src.session_cleaning import SessionCleaning
from src.features_extractor import FeaturesExtractor
from src.preparation_system_configuration import PreparationSystemConfiguration
from utility.json_handler import JsonHandler

CONFIG_PATH = './data/preparation_system_config.json'
CONFIG_SCHEMA_PATH = './data/preparation_system_config_schema.json'

'''
Module Name: PreparationSystem
Description: This class acts as a controller for the system.
'''
class PreparationSystem:
    """
    Class that controls the execution of the Preparation System 
    calling all the necessary functions to produce
    the prepared session from the raw one.
    """

    def __init__(self) -> None:
        """
        Initializes the PreparationSystem class, validates 
        the configuration and sets the instance variables
        for raw and prepared sessions.
        """
        try:
            self.configuration = PreparationSystemConfiguration(CONFIG_PATH, CONFIG_SCHEMA_PATH)
        except ValidationError:
            logging.error('Error during the Preparation System initialization phase')
            sys.exit()
        print(f'[+] The configuration is valid, {self.configuration.operative_mode} mode')
        self.raw_session = None
        self.prepared_session = None

    def run(self) -> None:
        """
        Method that runs all the instructions needed for session preparation.
        It continuously listens for new raw sessions, processes them, extracts features,
        prepares the session and sends it to the corresponding endpoint based on 
        the current operating mode.
        :return: None
        """
        # Create an instance of SessionCleaning
        cleaner = SessionCleaning()
         # Create an instance of JsonHandler
        json_handler = JsonHandler()

        # Start the Flask app listener on the port specified
        listener_thread = Thread(target=JsonIO.get_instance().listener, \
                                 args=('0.0.0.0', 5000), daemon=True)
        listener_thread.start()
        while JsonIO.get_instance().receive() is False:
            time.sleep(3)
        while True:
            # Get received raw session
            self.raw_session = JsonIO.get_instance().receive()
            print('[+] Raw session received')
            # Check raw session validity
            if json_handler.validate_json_data_file(self.raw_session, \
                                                    "./data/raw_session_schema.json"):
                print('[+] Raw session is valid')
            else:
                print('[-] Raw session is not valid')
                continue

            # Correct missing samples
            if cleaner.correct_missing_samples(self.raw_session['time_series']):
                print('[+] Pressure time series ok')
            else:
                print('[-] Missing samples are unrecoverable, raw session discarded')
                continue
            # Correct outliers
            cleaner.correct_outliers(self.raw_session['time_series'])

            # Extract features and prepare session
            self.prepared_session = {}
            FeaturesExtractor().extract_features \
                (self.raw_session, self.prepared_session)
            print('[+] Features extracted and session prepared')

            # Send prepared session to the endpoint corresponding to the current operating mode
            if self.configuration.operative_mode == 'development':
                if JsonIO.get_instance().send(self.prepared_session,
                                              "segregation"):
                    print(f'[+] Prepared session sent at \
                          {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

            elif self.configuration.operative_mode == 'production':
                if JsonIO.get_instance().send(self.prepared_session,
                                              "production"):
                    print(f'[+] Prepared session sent at \
                          {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

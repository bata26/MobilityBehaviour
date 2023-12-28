import os
import json

from jsonschema import validate, ValidationError
from threading import Thread

from src.json_io import JsonIO
import logging
from src.raw_session_integrity import RawSessionIntegrity
from src.raw_sessions_store import RawSessionsStore
from IngestionSystem.utility.json_handler import load_json, validate_json_file_file
from models.raw_session import RawSession

CONFIG_FILENAME = 'ingestion_system_config.json'
CONFIG_SCHEMA_FILENAME = 'ingestion_system_config_schema.json'


class IngestionSystem:
    """
    This class acts as a controller for the system
    """

    def __init__(self) -> None:
        """
        Initializes the system
        """

        if validate_json_file_file(CONFIG_FILENAME,CONFIG_SCHEMA_FILENAME):
            self.ingestion_system_config = load_json(CONFIG_FILENAME)
        else:
            logging.error('Error during the Ingestion System initialization phase')
            exit(-1)

    def run(self) -> None:
        """
        Runs the Ingestion System main process
        """

        # Run REST server
        listener = Thread(target=JsonIO.get_instance().listen, args=('0.0.0.0', 4000), daemon=True)
        listener.start()
        RawSession.receive_session()
        

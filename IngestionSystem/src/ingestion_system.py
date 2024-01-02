from jsonschema import ValidationError
from threading import Thread
from src.json_io import JsonIO
import logging
from src.raw_session_integrity import RawSessionIntegrity
from src.raw_sessions_store import RawSessionsStore
from models.ingestion_system_configuration import IngestionSystemConfiguration

CONFIG_PATH = './../data/ingestion_system_config.json'
CONFIG_SCHEMA_PATH = './../data/ingestion_system_config_schema.json'


class IngestionSystem:
    """
    This class acts as a controller for the system
    """

    def __init__(self) -> None:
        """
        Initializes the system
        """
        try:
            self.configuration = IngestionSystemConfiguration(CONFIG_PATH, CONFIG_SCHEMA_PATH)
        except ValidationError:
            logging.error('Error during the Ingestion System initialization phase')
            exit(-1)
        
        print(f'[+] The configuration is valid, {self.configuration["operative_mode"]} mode')
        
        self.last_uuid_received = None
        self.evaluation = False
        self.sessions_to_evaluation = 0
        self.sessions_to_produce = 0
            

    def run(self) -> None:
        """
        Runs the Ingestion System main process
        """
        operative_mode = self.configuration["operative_mode"]
        logging.info(f'Operative Mode: {operative_mode}', 2)

        # Create an instance of RawSessionsStore
        raw_sessions_store = RawSessionsStore()

        # Run REST server
        listener = Thread(target=JsonIO.get_instance().listen, args=('0.0.0.0', 4000), daemon=True)
        listener.start()

        while True:
            # Wait for a new record
            received_record = JsonIO.get_instance().receive()

            last_missing_sample = False
            if raw_sessions_store.store_record(record=received_record):
                if self.last_uuid_received is not None:
                    if self.last_uuid_received == received_record['uuid']:
                        # Check on the current session
                        session_complete = raw_sessions_store.is_session_complete(uuid=received_record['uuid'],
                                                                                  operative_mode=operative_mode,
                                                                                  last_missing_sample=False,
                                                                                  evaluation=self.evaluation)
                        uuid = received_record['uuid']
                    else:
                        # Check on the previous session because of a missing sample
                        logging.warning(f'Raw Session {self.last_uuid_received} missing sample detected')
                        session_complete = raw_sessions_store.is_session_complete(uuid=self.last_uuid_received,
                                                                                  operative_mode=operative_mode,
                                                                                  last_missing_sample=True,
                                                                                  evaluation=self.evaluation)
                        uuid = self.last_uuid_received
                        self.last_uuid_received = received_record['uuid']
                        last_missing_sample = True

                    if session_complete:
                        # If the session is complete there is no need for the next record to test "is_session_complete"
                        self.last_uuid_received = None
                        logging.success(f'Raw Session {uuid} complete')

                        # Load Raw Session from the Data Store
                        raw_session = raw_sessions_store.load_raw_session(uuid=uuid)

                        if raw_session['uuid'] is None:
                            continue

                        # Delete Raw Session from the Data Store
                        raw_sessions_store.delete_raw_session(uuid=uuid)

                        # Check Raw Session integrity
                        threshold = self.configuration['missing_samples_threshold']
                        raw_session_integrity = RawSessionIntegrity()
                        good_session = raw_session_integrity.mark_missing_samples(headset_eeg=raw_session['headset'],
                                                                                  threshold=threshold)

                        if good_session:
                            # Send Raw Session to the Preparation System
                            preparation_system_ip = self.configuration['preparation_system_ip']
                            preparation_system_port = self.configuration['preparation_system_port']
                            sent_to_preparation = JsonIO.get_instance().send(endpoint_ip=preparation_system_ip,
                                                                             endpoint_port=preparation_system_port,
                                                                             data=raw_session)

                            if sent_to_preparation:
                                logging.info(f'Raw Session {uuid} sent to the Preparation System', 0)

                            if self.evaluation:
                                # Send Raw Session to the Preparation System
                                evaluation_system_ip = self.configuration['evaluation_system_ip']
                                evaluation_system_port = self.configuration['evaluation_system_port']
                                label = {'uuid': raw_session['uuid'], 'label': raw_session['pressure_detected']}
                                sent_to_evaluation = JsonIO.get_instance().send(endpoint_ip=evaluation_system_ip,
                                                                                endpoint_port=evaluation_system_port,
                                                                                data=label)
                                if sent_to_evaluation:
                                    logging.info(f'Label "{raw_session["command_thought"]}" sent to the evaluation System', 1)
                                    self.sessions_to_evaluation += 1
                                    logging.trace(f'Labels to sent to the evaluation System: {self.sessions_to_evaluation}')

                                    if self.sessions_to_evaluation == self.configuration['evaluation_window']:
                                        self.sessions_to_evaluation = 0
                                        self.evaluation = False
                                        logging.trace(f'evaluation phase ended')
                            else:
                                if self.configuration['operative_mode'] == 'execution':
                                    self.sessions_to_produce += 1
                                    logging.trace(f'Sessions executed: {self.sessions_to_produce}')

                                    if self.sessions_to_produce == self.configuration['production_window']:
                                        self.evaluation = True
                                        self.sessions_to_produce = 0
                                        logging.trace('Entering in evaluation phase')
                        else:
                            logging.error(f'Raw Session {uuid} discarded [threshold not satisfied]')
                    else:
                        if last_missing_sample:
                            logging.error(f'Raw Session {uuid} not complete [no recovery possible]')
                            # Session not complete (meaning that some required record is missing)
                            # Being last_missing_samples equal to True, the system will not receive any other record
                            # related to this session (session is lost) so it must be deleted from the data store
                            raw_sessions_store.delete_raw_session(uuid=uuid)
                            self.last_uuid_received = None
                else:
                    self.last_uuid_received = received_record['uuid']
        

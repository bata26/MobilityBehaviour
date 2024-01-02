from src.raw_sessions_store import RawSessionsStore
from src.json_io import JsonIO
import logging
from src.raw_session_integrity import RawSessionIntegrity
from models.ingestion_system_configuration import IngestionSystemConfiguration

class RawSession:
    def __init__(self, uuid: str,
                 label: str,
                 time_series: list,
                 calendar: str,
                 environment: str):
        self.uuid = uuid
        self.pressure_detected = label
        self.time_series = time_series
        self.calendar = calendar
        self.environment = environment

    def receive_session(self) -> None:
        last_uuid_received = None
        evaluation = False
        sessions_to_evaluation = 0
        sessions_to_production = 0

        config = IngestionSystemConfiguration()
        operative_mode = config['operative_mode']
        logging.info(f'Operative Mode: {operative_mode}', 2)
        
        # Create an instance of RawSessionsStore
        raw_sessions_store = RawSessionsStore()

        while True:
            # Wait for a new record
            received_record = JsonIO.get_instance().receive()

            last_missing_sample = False
            if raw_sessions_store.store_record(record=received_record):
                if last_uuid_received is not None:
                    if last_uuid_received == received_record['uuid']:
                        # Check on the current session
                        session_complete = raw_sessions_store.is_session_complete(uuid=received_record['uuid'],
                                                                                  operative_mode=operative_mode,
                                                                                  last_missing_sample=False,
                                                                                  evaluation=evaluation)
                        uuid = received_record['uuid']
                    else:
                        # Check on the previous session because of a missing sample
                        logging.warning(f'Raw Session {last_uuid_received} missing sample detected')
                        session_complete = raw_sessions_store.is_session_complete(uuid=last_uuid_received,
                                                                                  operative_mode=operative_mode,
                                                                                  last_missing_sample=True,
                                                                                  evaluation=evaluation)
                        uuid = last_uuid_received
                        last_uuid_received = received_record['uuid']
                        last_missing_sample = True

                    if session_complete:
                        # If the session is complete there is no need for the next record to test "is_session_complete"
                        last_uuid_received = None
                        logging.success(f'Raw Session {uuid} complete')

                        # Load Raw Session from the Data Store
                        raw_session = raw_sessions_store.load_raw_session(uuid=uuid)

                        if raw_session['uuid'] is None:
                            continue

                        # Delete Raw Session from the Data Store
                        raw_sessions_store.delete_raw_session(uuid=uuid)

                        # Check Raw Session integrity
                        threshold = config['missing_samples_threshold']
                        raw_session_integrity = RawSessionIntegrity()
                        good_session = raw_session_integrity.mark_missing_samples(time_series=raw_session['time_series'],
                                                                                  threshold=threshold)

                        if good_session:
                            # Send Raw Session to the Preparation System
                            preparation_system_ip = config['preparation_system_ip']
                            preparation_system_port = config['preparation_system_port']
                            sent_to_preparation = JsonIO.get_instance().send(endpoint_ip=preparation_system_ip,
                                                                             endpoint_port=preparation_system_port,
                                                                             data=raw_session)

                            if sent_to_preparation:
                                logging.info(f'Raw Session {uuid} sent to the Preparation System', 0)

                            if evaluation:
                                # Send Raw Session to the Evaluation System
                                evaluation_system_ip = config['evaluation_system_ip']
                                evaluation_system_port = config['evaluation_system_port']
                                label = {'uuid': raw_session['uuid'], 'label': raw_session['pressure_detected']}
                                sent_to_evaluation = JsonIO.get_instance().send(endpoint_ip=evaluation_system_ip,
                                                                                endpoint_port=evaluation_system_port,
                                                                                data=label)
                                if sent_to_evaluation:
                                    logging.info(f'Label "{raw_session["pressure_detected"]}" sent to the evaluation System', 1)
                                    sessions_to_evaluation += 1
                                    logging.trace(f'Labels to sent to the evaluation System: {sessions_to_evaluation}')

                                    if sessions_to_evaluation == config['evaluation_window']:
                                        sessions_to_evaluation = 0
                                        evaluation = False
                                        logging.trace(f'evaluation phase ended')
                            else:
                                if config['operative_mode'] == 'production':
                                    sessions_to_production += 1
                                    logging.trace(f'Sessions executed: {self.sessions_to_execute}')

                                    if sessions_to_production == config['production_window']:
                                        evaluation = True
                                        sessions_to_production = 0
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
                            last_uuid_received = None
                else:
                    last_uuid_received = received_record['uuid']
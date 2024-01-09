import sys
import logging
from typing import Any
from threading import Thread
import queue
from flask import Flask, request
from requests import post, exceptions
from jsonschema import ValidationError
from src.ingestion_system_configuration import IngestionSystemConfiguration

CONFIG_PATH = './data/ingestion_system_config.json'
CONFIG_SCHEMA_PATH = './data/ingestion_system_config_schema.json'

class JsonIO:
    """
    This class implements the methods for receiving records and
    sending the raw sessions to the Preparation System.
    """
    instance = None
    def __init__(self) -> None:
        """
        Initializes the JsonIO object
        """
        self.app = Flask(__name__)
        self.received_records_queue = queue.Queue()
        try:
            self.configuration = IngestionSystemConfiguration(CONFIG_PATH, CONFIG_SCHEMA_PATH)
        except ValidationError:
            sys.exit(1)

    @staticmethod
    def get_instance() -> Any:
        """
        :return: instance of the JsonIO class
        """
        if JsonIO.instance is None:
            JsonIO.instance = JsonIO()
        return JsonIO.instance

    def get_app(self) -> Any:
        """
        :return: instance of the app Flask
        """
        return self.app

    def put_received_record(self, received_record: dict) -> bool:
        """
        Receives a record and enqueues it in a thread-safe queue
        :param received_record: record sent from a data source
        (calendar, labels, settings, pressure time series)
        :return: True if the record is entered correctly. False if the insertion fails.
        """
        try:
            self.received_records_queue.put(received_record, timeout=None)
            # with open(os.path.join(os.path.abspath('..'), 'data', 'queue_size.txt'), 'w') as f:
            #    f.write(f'{self.received_records_queue.qsize()}')
        except queue.Full:
            logging.error('Full queue exception')
            return False
        return True

    def send_to_main(self):
        self.received_records_queue.put(True, block=True)

    def receive(self) -> Any:
        """
        Extracts a record from the queue containing all the received records
        :return: record
        """
        return self.received_records_queue.get(block=True)

    def send(self, data: dict, dest_system: str) -> bool:
        """
        Sends data to other systems
        :param data: dictionary containing the data to send
        :dest_system: destination system
        :return: True if the 'send' is successful. False otherwise.
        """
        try:
            if dest_system == "preparation":
                connection_string = f'http://{self.configuration.preparation_system_ip}:{self.configuration.preparation_system_port}/json'
            elif dest_system == "evaluation":
                connection_string = f'http://{self.configuration.evaluation_system_ip}:{self.configuration.evaluation_system_port}/expertLabels'
            response = post(url=connection_string, json=data, timeout=3)
        except exceptions.RequestException:
            logging.error('%s unreachable', connection_string)
            sys.exit(1)

        if response.status_code != 200:
            error_message = response.json()['error']
            logging.error('Error: %s', error_message)
            return False

        return True

    def listen(self, ip: str, port: int) -> None:
        """
        Runs the application server
        :param ip: IP of the local server
        :param port: Port of the local server
        :return: None
        """
        self.app.run(host=ip, port=port, debug=False)



app = JsonIO.get_instance().get_app()
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.post('/record')
def post_json():
    """
    Flask view function that handles requests related to records 
    sent from the different data sources
    """
    if request.json is None:
        return {'error': 'No record received'}, 500

    received_record = request.json
    new_thread = Thread(target=JsonIO.get_instance().put_received_record, args=(received_record, ))
    new_thread.start()

    return {}, 200

@app.get('/start')
def start_system():
    """
    The function is called when a post request is received on the json endpoint.
    This function starts the entire system.
    :return: Returns a JSON response with status code 200 if the request is successful,
            and with status code 500 if it's not.
    """
    print("[INFO] Start msg received")
    receive_thread = Thread(target=JsonIO.get_instance().send_to_main)
    receive_thread.start()
    return {}, 200

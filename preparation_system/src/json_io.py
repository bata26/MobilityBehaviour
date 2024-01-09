import sys
import queue
import logging
from typing import Any
from threading import Thread
from flask import Flask, request
from requests import post, exceptions
from jsonschema import ValidationError
from src.preparation_system_configuration import PreparationSystemConfiguration

CONFIG_PATH = './data/preparation_system_config.json'
CONFIG_SCHEMA_PATH = './data/preparation_system_config_schema.json'

class JsonIO:
    """
    JsonIO is a class that provides functionality for sending and receiving JSON payloads.
    It uses Flask to handle incoming JSONs and the requests library to send them to other endpoints.
    """
    json_io_instance = None

    def __init__(self) -> None:
        """
        Initializes a new JsonIO instance and creates a Flask application and a queue for storing
        received JSON payloads.
        """
        try:
            self.configuration = PreparationSystemConfiguration(CONFIG_PATH, CONFIG_SCHEMA_PATH)
        except ValidationError:
            sys.exit(1)
        self.app = Flask(__name__)
        self.received_json_queue = queue.Queue()

    @staticmethod
    def get_instance() -> Any:
        """
        :return: Instance of the JsonIO class
        """
        if JsonIO.json_io_instance is None:
            JsonIO.json_io_instance = JsonIO()
        return JsonIO.json_io_instance

    def get_app(self) -> Any:
        """
        :return: instance of the app Flask
        """
        return self.app

    def listener(self, ip, port) -> None:
        """
        Starts the listener on the specified IP and port.
        :param ip: IP address to listen on.
        :param port: Port to listen on.
        :return: None
        """
        self.app.run(host=ip, port=port, debug=False)

    def receive(self) -> Any:
        """
        Retrieves a raw session or the start message 
        from the received JSON queue.
        :return: Raw session
        """
        return self.received_json_queue.get(block=True)

    # -------- SERVER HANDLER --------

    def put_received_record(self, received_json) -> bool:
        """
        Adds the received JSON payload to _received_json_queue.
        :param received_json: JSON payload received by the server.
        :return: None
        """
        # If the queue is full the thread is blocked
        try:
            self.received_json_queue.put(received_json, timeout=5)
        except queue.Full:
            print("Full queue exception")
            return False
        return True

    def send_to_main(self):
        self.received_json_queue.put(True, block=True)

    # -------- CLIENT REQUEST --------
    def send(self, json_to_send: dict, dest_system: str) -> bool:
        """
        Sends a JSON payload to a specified endpoint.
        :param json_to_send: The JSON payload to send.
        :dest_system: destination system
        :return: True if the payload is sent successfully, False otherwise.
        """
        try:
            if dest_system == "production":
                connection_string = \
                    f'http://{self.configuration.production_system_ip}:{self.configuration.production_system_port}/preparedsession'
            elif dest_system == "segregation":
                connection_string = \
                    f'http://{self.configuration.segregation_system_ip}:{self.configuration.segregation_system_port}/preparedsession'
            response = post(connection_string, json=json_to_send, timeout=5)
            if response.status_code != 200:
                error_message = response.json()['error']
                print(f'[-] Error: {error_message}')
                return False
        except exceptions.RequestException as e:
            print(f'[-] Connection Error (endpoint unreachable): {e}')
            sys.exit(1)
        return True

app = JsonIO.get_instance().app
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.post('/json')
def post_json():
    """
    The function is called when a post request is received on the json endpoint.
    :return: Returns a JSON response with status code 200 if the request is successful,
            and with status code 500 if it's not.
    """
    if request.json is None:
        return {'error': 'No JSON received'}, 500

    received_json = request.json

    new_thread = Thread(target=JsonIO.get_instance().put_received_record, args=(received_json,))
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

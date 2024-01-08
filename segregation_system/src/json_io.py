import queue
from threading import Thread
from flask import Flask, request
from requests import post, exceptions
import logging

log = logging.getLogger('werkzeug')
log.disabled = True
class JsonIO:

    _instance = None

    def __init__(self):
        # Flask instance to receive data
        self._app = Flask(__name__)
        # a thread-safe queue to buffer the received json message
        self._received_json_queue = queue.Queue()

    @staticmethod
    def get_instance():
        if JsonIO._instance is None:
            JsonIO._instance = JsonIO()
        return JsonIO._instance

    def listener(self, ip, port):
        # execute the listening server, for each message received, it will be handled by a thread
        self._app.run(host=ip, port=port, debug=False, threaded=True)

    def get_app(self):
        return self._app

    def send_to_main(self):
        self._received_json_queue.put(True, block=True)

    def get_queue(self):
        return self._received_json_queue

    def receive(self):
        # get json message from the queue
        # if the queue is empty the thread is blocked
        return self._received_json_queue.get(block=True)

    def put_json_into_queue(self, received_json):
        # save received message into queue
        self._received_json_queue.put(received_json)

    def send(self, ip, port, endpoint, data):
        url = f'http://{ip}:{port}/' + endpoint
        response = None
        try:
            response = post(url, json=data, timeout=10.0)
        except exceptions.RequestException:
            print("Endpoint system unreachable")
            return False

        if response.status_code != 200:
            res = response.json()
            error_message = 'unknown'
            if 'error' in res:
                error_message = res['error']
            print(f'Sending Error: {error_message}')
            return False

        return True


app = JsonIO.get_instance().get_app()

@app.get('/start')
def start_app():
    print("[INFO] Start msg received")
    receive_thread = Thread(target=JsonIO.get_instance().send_to_main)
    receive_thread.start()
    return {}, 200

@app.post('/preparedsession')
def post_json():
    if request.json is None:
        return {'error': 'No JSON received'}, 500

    received_json = request.json
    JsonIO.get_instance().put_json_into_queue(received_json)
    return {}, 200

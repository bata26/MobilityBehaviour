import queue
from threading import Thread
from dotenv import load_dotenv
from flask import Flask, request

from model.msg_configuration import MessageConfiguration

load_dotenv()


class MessageManager:
    _instance = None

    def __init__(self):
        self._configuration = MessageConfiguration()
        self._app = Flask(__name__)
        self._queue = queue.Queue()

    @staticmethod
    def get_instance():
        if MessageManager._instance is None:
            MessageManager._instance = MessageManager()
        return MessageManager._instance

    def start_server(self):
        print("[INFO] Starting API...")
        self._app.run(
            host=self._configuration.host_src_ip,
            port=self._configuration.host_src_port,
            debug=False,
        )

    def get_app(self):
        return self._app

    def receive(self):
        # get json message from the queue
        return self._queue.get(block=True)

    def send_label(self, label_dict):
        self._queue.put(label_dict, block=True)

    def send_start(self):
        self._queue.put(True, block=True)
        print('[INFO] Start signal received')


app = MessageManager.get_instance().get_app()


@app.post('/expertLabels')
def receive_expert_labels():
    if request.json is None:
        return {'[ERROR] No Payload Received'}, 500
    print(request.json)
    received_json = request.json
    received_json['source'] = 'expert'  # Add 'source' attribute with the value 'expert'

    receive_thread = Thread(target=MessageManager.get_instance().send_label, args=(received_json,))
    receive_thread.start()

    return {}, 200


@app.post('/classifierLabels')
def receive_classifier_labels():
    if request.json is None:
        return {'[ERROR] No Payload Received'}, 500
    received_json = request.json
    received_json['source'] = 'classifier'  # Add 'source' attribute with the value 'classifier'

    receive_thread = Thread(target=MessageManager.get_instance().send_label, args=(received_json,))
    receive_thread.start()
    return {}, 200

@app.get('/start')
def start_app():
    receive_thread = Thread(target=MessageManager.get_instance().send_start)
    receive_thread.start()
    return {}, 200

import queue
import logging
import os
from threading import Thread
from dotenv import load_dotenv
from model.msg_configuration import MessageConfiguration
from flask import Flask, request
from model.prepared_session import PreparedSession
import requests as r


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
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
        print("[INFO] Starting Rest server...")
        self._app.run(
            host = self._configuration.host_src_ip,
            port=self._configuration.host_src_port,
            debug=False,
        )
    def get_app(self):
        return self._app

    def get_queue(self):
        return self._queue

    def send_classifier(self):
        self._queue.put(True, block=True)
        print('New Classifier received')

    def send_prepared_session(self , received_prepared_session):
        prepared_session = PreparedSession(received_prepared_session)
        self._queue.put(prepared_session, block=True)
        print('New prepared session received')

    def send_post_request(self , dest, data):
        if dest == "EVALUATION":
            uri = "http://" + self._configuration.evaluation_system_ip + ":" + self._configuration.evaluation_system_port + "/"
        elif dest == "CLIENT":
            uri = "http://" + self._configuration.client_system_ip + ":" + self._configuration.client_system_port + "/"
        else:
            uri = "http://" + self._configuration.messaging_system_ip + ":" + self._configuration.messaging_system_port + "/"
        try:
            res = r.post(uri , json=data, timeout=5)
            if res.status_code == 200:
                print(f"[INFO] Labels correctly sended to {dest} system")
            else:
                print(f"[ERROR] Impossible to send labels to {dest} system")
        except TimeoutError:
            print(f"[ERROR] {dest} system is unavailable, timeout")


app = MessageManager.get_instance().get_app()

@app.post('/deploy')
def deploy():
    f = request.files['file']
    f.save(os.getenv("CLASSIFIER_FILE_PATH"))
    receive_thread = Thread(target=MessageManager.get_instance().send_classifier)
    receive_thread.start()
    return {}, 200

@app.post('/preparedsession')
def receive_prepared_session():
    if request.json is None:
        return {'error': 'No Payload Received'}, 500

    received_json = request.json
    print("[DEBUG] received json : " , received_json)
    receive_thread = Thread(target=MessageManager.get_instance().send_prepared_session , args = (received_json,))
    receive_thread.start()
    return {}, 200

import os
import queue
import logging
from dotenv import load_dotenv
from threading import Thread

from model.msg_configuration import MessageConfiguration
from flask import Flask, request
import requests



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

    def send_to_main(self , dataset):
        self._queue.put(dataset, block=True)
        print('New Dataset received')

    def send_classifier(self , uuid):
        url = f"http://{self._configuration.host_dest_ip}:{self._configuration.host_dest_port}/deploy"
        file_path = os.getenv("CLASSIFIER_DIRECTORY_PATH") + uuid + ".joblib"
        file = {'file': open(file_path,'rb')}

        try:
            r = requests.post(url, files=file , timeout=3)
            if r.status_code == 200:
                print("[INFO] Correctly deployed classifier")
            else:
                print("[ERROR] Impossible to deploy classifier")
                raise Exception("Impossible to deploy classifier")
        except TimeoutError:
            print("[ERROR] Timeout")
            raise TimeoutError

app = MessageManager.get_instance().get_app()

@app.post('/senddata')
def post_json():
    if request.json is None:
        return {'error': 'No Payload Received'}, 500

    received_json = request.json
    #print("REQUEST BODY : " , received_json)
    receive_thread = Thread(target=MessageManager.get_instance().send_to_main, args=(received_json,))
    receive_thread.start()
    #receive_thread = Thread(target=JsonIO.get_instance().receive, args=(received_json,))
    #receive_thread.start()
    return {}, 200

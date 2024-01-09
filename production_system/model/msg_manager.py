import queue
import logging
import time
import os
from threading import Thread
from dotenv import load_dotenv
from model.msg_configuration import MessageConfiguration
from flask import Flask, request
from model.prepared_session import PreparedSession
import requests as r
from marshmallow import Schema, fields, validate

class DeploySchema(Schema):
    file = fields.Field(required=True)
class FeaturesSchema(Schema):
    maximum_pressure_ts = fields.Float(required=True)
    minimum_pressure_ts = fields.Float(required=True)
    median_pressure_ts = fields.Float(required=True)
    mean_absolute_deviation_pressure_ts = fields.Float(required=True)
    activity_and_small_scatter = fields.Float(required=True)
    environment_and_small_scatter = fields.Float(required=True)

class PreparedSessionSchema(Schema):
    _id = fields.Str(required=True)
    calendar = fields.Str(required=True)
    environment = fields.Str(required=True)
    label = fields.Str(required=True)
    features = fields.Nested(FeaturesSchema, required=True)

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

    def send_to_main(self):
        self._queue.put(True, block=True)
        print('New Classifier received')

    def send_prepared_session(self , received_prepared_session):
        prepared_session = PreparedSession(received_prepared_session)
        self._queue.put(prepared_session, block=True)
        print('New prepared session received')

    def send_post_request(self , dest, data):
        if dest == "EVALUATION":
            uri = "http://" + self._configuration.evaluation_system_ip + ":" + str(self._configuration.evaluation_system_port) + "/classifierLabels"
        elif dest == "CLIENT":
            uri = "http://" + self._configuration.client_system_ip + ":" + str(self._configuration.client_system_port) + "/"
            print(f"[INFO] Send result to client at url : {uri}")
        else:
            uri = "http://" + self._configuration.messaging_system_ip + ":" + str(self._configuration.messaging_system_port) + "/"
            print(f"[INFO] Send result to messaging at url : {uri}")
            return
        try:
            res = r.post(uri , json=data, timeout=5)
            if res.status_code == 200:
                print(f"[INFO] Labels correctly sended to {dest} system")
            else:
                print(f"[ERROR] Impossible to send labels to {dest} system")
        except TimeoutError:
            print(f"[ERROR] {dest} system is unavailable, timeout")


app = MessageManager.get_instance().get_app()


@app.get('/start')
def start_app():
    print("[INFO] Start msg received")
    receive_thread = Thread(target=MessageManager.get_instance().send_to_main)
    receive_thread.start()
    return {}, 200

@app.post('/deploy')
def deploy():
    schema = DeploySchema()
    errors = schema.validate(request.files)

    if errors:
        return errors, 400

    f = request.files['file']
    f.save(os.getenv("CLASSIFIER_FILE_PATH"))
    receive_thread = Thread(target=MessageManager.get_instance().send_classifier)
    receive_thread.start()
    return {}, 200

@app.post('/preparedsession')
def receive_prepared_session():
    if request.json is None:
        return {'error': 'No Payload Received'}, 500

    schema = PreparedSessionSchema()
    errors = schema.validate(request.json)

    if errors:
        return errors, 400

    received_json = request.json
    print("[DEBUG] received json : " , received_json)
    receive_thread = Thread(target=MessageManager.get_instance().send_prepared_session , args = (received_json,))
    receive_thread.start()
    return {}, 200

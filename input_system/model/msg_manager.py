import os
import queue
import logging
from threading import Thread
from dotenv import load_dotenv
from flask import Flask, request
import requests
from model.msg_configuration import MessageConfiguration
from marshmallow import Schema, fields

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
load_dotenv()

class LabelSchema(Schema):
    uuid = fields.String(required=True)
    label = fields.String(required=True)

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

    def send_to_main(self):
        self._queue.put(True, block=True)
        print('New Dataset received')

    def send_data(self, json):
        uri = "http://" + self._configuration.host_dest_ip + ":" + str(self._configuration.host_dest_port) + "/record"
        try:
            res = requests.post(uri, json=json, timeout=3)
            if res.status_code != 200:
                raise Exception("[ERROR] Not received 200")
        except Exception as e:
            raise e
app = MessageManager.get_instance().get_app()

@app.get('/start')
def post_json():
    print("[INFO] Start msg received")
    receive_thread = Thread(target=MessageManager.get_instance().send_to_main)
    receive_thread.start()
    return {}, 200

@app.post("/label")
def post_label():
    schema = LabelSchema()
    errors = schema.validate(request.json)

    if errors:
        return errors, 400
    print("[INFO] Received Label")

from threading import Thread
import time

from model.msg_manager import MessageManager
from model.system_configuration import SystemConfiguration
from model.json_validator import JsonValidator
from utils.json_reader import JsonReader
from model.label_storage import LabelStorage


class EvaluationSystem:

    def __init__(self):
        print("[INFO] Starting Evaluation System...")
        print("[INFO] Loading Configuration...")
        read_result, file_content = JsonReader.read_json_file("data/system_configuration.json")
        if not read_result:
            print("[ERROR] Couldn't read system configuration")
            return
        JsonValidator.validate_schema(file_content, "system_configuration")
        self.config = SystemConfiguration(None)
        self.label_storage = LabelStorage(self.config)
        print("[INFO] CONFIGURATION DONE")

    def run(self):

        run_thread = Thread(target=MessageManager.get_instance().start_server)
        run_thread.setDaemon(True)
        run_thread.start()

        while MessageManager.get_instance().receive() is not True:
            time.sleep(3)

        while True:
            print("[INFO] Creating label tables...")
            self.label_storage.create_tables()
            print("[INFO] Waiting for label...")
            received_label = MessageManager.get_instance().receive()
            print("[INFO] Label received")
            self.label_storage.store_label(received_label)


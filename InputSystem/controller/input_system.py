from threading import Thread
import time
import sys
from jsonschema import ValidationError
from model.msg_manager import MessageManager
from model.system_configuration import SystemConfiguration
from model.json_validator import JsonValidator
from model.dataset import Dataset

class InputSystem:
    def __init__(self):
        print("[INFO] STARTING SYSTEM...")
        try:
            JsonValidator.validate_schemas()
        except ValidationError:
            print("[ERROR] Impossible to validate configuration file, exit")
            sys.exit(1)
        self._configuration = SystemConfiguration()
        print("[INFO] CONFIGURATION DONE")
        print("[DEBUG] Interval " , self._configuration.interval)
        try:
            Dataset.fill_db()
        except Exception as e:
            print("[ERROR] " , str(e))

    def run(self):

        run_thread = Thread(target=MessageManager.get_instance().start_server)
        run_thread.setDaemon(True)
        run_thread.start()

        while MessageManager.get_instance().get_queue().get(block=True) is False:
            time.sleep(3)

        while True:
            if self._configuration.situation == "ideal":
                Dataset.send_ideal_data(self._configuration.interval)
            else:
                Dataset.send_real_data(self._configuration.interval, self._configuration.probability)
            break
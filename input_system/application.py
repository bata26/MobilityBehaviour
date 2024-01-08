import sys
import os
import signal
from dotenv import load_dotenv
from controller.input_system import InputSystem
from utils.json_reader import JsonReader

def handler(signum, frame):
    print("[INFO] Received ctrl + c signal, interrupt and reset application")
    JsonReader.update_json_file(os.getenv("CONFIG_FILE_PATH") , "stage" , "waiting")
    sys.exit(1)

signal.signal(signal.SIGINT, handler)

load_dotenv()
if __name__ == '__main__':
    InputSystem().run()

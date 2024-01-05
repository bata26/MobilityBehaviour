import sys
import os
import time
import signal
from dotenv import load_dotenv
from controller.development_system import DevelopmentSystem
from utils.json_reader import JsonReader

def handler(signum, frame):
    print("[INFO] Received ctrl + c signal, interrupt and reset application")
    JsonReader.update_json_file(os.getenv("CONFIG_FILE_PATH") , "stage" , "waiting")
    sys.exit(1)

signal.signal(signal.SIGINT, handler)


load_dotenv()
if __name__ == '__main__':
    start_time = time.time()
    DevelopmentSystem().run(True)
    end_time = time.time()
    print("START : " , start_time)
    print("END : " , end_time)

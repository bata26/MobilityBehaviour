from threading import Thread
import os

from model.msg_manager import MessageManager
from model.system_configuration import SystemConfiguration
from model.classifier import Classifier
from controller.training_controller import TrainingController
from controller.validation_controller import ValidationController
from model.dataset import Dataset
from utils.json_reader import JsonReader
from controller.test_controller import TestController

class DevelopmentSystem:
    def __init__(self):
        print("[INFO] STARTING SYSTEM...")
        self._configuration = SystemConfiguration()
        print("[INFO] CONFIGURATION DONE")
    def run(self):

        print("[DEBUG] TEST DATASET")
        #read_result , file_content = JsonReader.read_json_file("./json/request-example.json")
        #if not read_result:
        #    return
        # start the rest server in a new thread as daemon
        run_thread = Thread(target=MessageManager.get_instance().start_server)
        run_thread.setDaemon(True)
        run_thread.start()

        dataset = MessageManager.get_instance().get_queue().get(block=True)
        Dataset.set_data(dataset)

        print("[INFO] Fetching Classifier Configuration")
        print("[INFO] Setup Train Classifier")
        train_controller = TrainingController()
        print("[INFO] Classifier correctly created")
        print("[INFO] Set average hyperparameters")
        train_controller.set_average_hyperparameters()
        print("[INFO] Set average hyperparameters ended")

        if self._configuration.starting_mode == "waiting" :
            inserted_iterations = int(input("[HUMAN] Insert number of iterations\n"))

        train_controller.update_iterations_number(inserted_iterations)
        print("[INFO] Start Training Classifier")
        train_controller.start_training()

        if self._configuration.ongoing_validation is True:
            print("[INFO] Ongoing validation is true")
        else:
            print("[INFO] Exported chart, waiting for human to check learning plot")

            if self._configuration.flow["learning_plot_result"] is True:
                print("[INFO] Set hyperparams")
                validation_controller = ValidationController()
                validation_controller.validate_classifier()
                validation_controller.generate_validation_report()
                uuid = input("[HUMAN] Insert the UUID of the winner classifier\n")
                validation_controller.select_classifier(uuid)
                test_controller = TestController()
                test_controller.evaluate_test_result()
                test_controller.generate_test_report()
        while True:
            pass

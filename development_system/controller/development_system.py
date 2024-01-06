from threading import Thread
import sys
import time
from jsonschema import ValidationError
from .test_controller import TestController
from model.json_validator import JsonValidator
from model.msg_manager import MessageManager
from model.system_configuration import SystemConfiguration
from controller.training_controller import TrainingController
from controller.validation_controller import ValidationController
from model.dataset import Dataset

STAGES = ["waiting" , "set_avg_hyp" , "set_nr_iter", "train", "set_hyp" ,"gen_lrng_rep" , "gen_vld_rep" , "gen_tst_rep" , "cnfg_sent" , "clsfr_sent", "ask_cnfg", "snd_clsfr"]

class DevelopmentSystem:
    def __init__(self):
        print("[INFO] STARTING SYSTEM...")
        try:
            JsonValidator.validate_schemas()
        except ValidationError:
            print("[ERROR] Impossible to validate configuration file, exit")
            sys.exit(1)
        self._configuration = SystemConfiguration()
        print("[INFO] CONFIGURATION DONE")
        self._train_controller = TrainingController()

    def update_stage(self , new_state):
        self._configuration.stage = new_state
        self._configuration.update_stage()

    def run(self, productivity = False):

        if productivity is False:
            run_thread = Thread(target=MessageManager.get_instance().start_server)
            run_thread.setDaemon(True)
            run_thread.start()

        while MessageManager.get_instance().get_queue().get(block=True) is False:
            time.sleep(3)

        while True:
            # RECEIVE DATASET
            if self._configuration.stage == "waiting":
                dataset = MessageManager.get_instance().get_queue().get(block=True)
                Dataset.set_data(dataset)
                self.update_stage("set_avg_hyp")

            # SET AVG HYPERPARAMS
            if self._configuration.stage == "set_avg_hyp":

                print("[INFO] Set average hyperparameters")
                self._train_controller.set_average_hyperparameters()
                print("[INFO] Set average hyperparameters ended")
                self.update_stage("set_nr_iter")

            if self._configuration.stage == "set_nr_iter":
                if productivity is True:
                    inserted_iterations = 100
                else:
                    inserted_iterations = int(input("[HUMAN] Insert number of iterations\n"))

                self._train_controller.update_iterations_number(inserted_iterations)
                print("[INFO] Start Training Classifier")
                self.update_stage("train")

            if self._configuration.stage == "train":
                self._train_controller.start_training()

            if self._configuration.ongoing_validation is True:
                self.update_stage("set_hyp")
            else:
                self.update_stage("gen_lrng_rep")

            if self._configuration.stage == "gen_lrng_rep":
                self._train_controller.generate_learning_report()
                print("[INFO] Exported chart, waiting for human to check learning plot")
                print("[HUMAN] Wait for checking the learning_plot")

                if productivity is True:
                    learning_res = "y"
                else:
                    learning_res = input("Is the number of iterations fine? (Y/n)\n")

                if learning_res == "Y" or learning_res == "y":
                    self.update_stage("set_hyp")
                    self._configuration.ongoing_validation = False
                elif learning_res == "n" or learning_res == "N":
                    self.update_stage("set_nr_iter")

            if self._configuration.stage == "set_hyp":
                print("[INFO] Set hyperparams")
                validation_controller = ValidationController()
                validation_controller.validate_classifier()
                validation_controller.generate_validation_report()
                uuid = input("[HUMAN] Insert the UUID of the winner classifier\n")

                if uuid == "":
                    self.update_stage("set_avg_hyp")
                else:
                    validation_controller.select_classifier(uuid)
                    self.update_stage("gen_tst_rep")

            if self._configuration.stage == "gen_tst_rep":
                test_controller = TestController()
                test_controller.evaluate_test_result()
                test_controller.generate_test_report()

                print("[INFO] Test Report Generated, waiting for human")
                if productivity is True:
                    test_res = "y"
                else:
                    test_res = input("[HUMAN] Is the test passed? (Y/n)\n")

                if test_res == "Y" or test_res == "y":
                    self.update_stage("snd_clsfr")
                elif test_res == "n" or test_res == "N":
                    self.update_stage("ask_cnfg")

                if productivity is True:
                    break

            if self._configuration.stage == "ask_cnfg":
                print("[WARN] Test not passed, needed new config")
                print("[WARN] Shutdown")
                self.update_stage("waiting")
                sys.exit(1)

            if self._configuration.stage == "snd_clsfr":
                print("[INFO] Test passed, send classifier to production system")
                try:
                    MessageManager.get_instance().send_classifier(uuid)
                    self.update_stage("waiting")
                except Exception as e:
                    print("[ERROR] Error : ", str(e))
                    sys.exit(1)

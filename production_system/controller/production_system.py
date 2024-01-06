from threading import Thread
import os

from model.msg_manager import MessageManager
from model.system_configuration import SystemConfiguration
from controller.deploy_controller import DeployController
from controller.classify_controller import ClassifyController
from model.json_validator import JsonValidator
class ProductionSystem:
    def __init__(self):
        print("[INFO] STARTING SYSTEM...")
        print("[INFO] Validate Json file...")
        JsonValidator.validate_schemas()
        self._configuration = SystemConfiguration()
        print("[INFO] CONFIGURATION DONE")

    def run(self):

        run_thread = Thread(target=MessageManager.get_instance().start_server)
        run_thread.setDaemon(True)
        run_thread.start()
        while True:
            print("[INFO] Waiting for classifier from develop system...")
            MessageManager.get_instance().get_queue().get(block=True)
            print("[INFO] Classifier received")
            print("[INFO] Starting deploy")
            deploy_controller = DeployController()
            deploy_controller.deploy_classifier()
            print("[INFO] Classifier deployed")
            MessageManager.get_instance().send_post_request("MESSAGING" , {"reset" : True})

            prepared_session = MessageManager.get_instance().get_queue().get(block=True)
            classify_controller = ClassifyController(prepared_session)
            classification_result = classify_controller.classify()
            print("[INFO] classification result: " , classification_result)

            if self._configuration.evaluation_phase is True:
                print("[DEBUG] To Evaluation Sys")
                MessageManager.get_instance().send_post_request("EVALUATION" , classification_result)
            MessageManager.get_instance().send_post_request("CLIENT" , classification_result)

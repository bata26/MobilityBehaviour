import os

from model.classifier import Classifier
from utils.json_reader import JsonReader
from generator.test_report_generator import TestReportGenerator
from model.dataset import Dataset


class TestManager:

    def __init__(self):
        self._classifier = Classifier()
        self._validation_data = Dataset.get_data("validation")
        self._test_data = Dataset.get_data("test")
        read_result, file_content = JsonReader.read_json_file(os.getenv("PICKED_CLASSIFIER_FILE_PATH"))
        if not read_result:
            return
        self._picked_uuid = file_content["uuid"]
        self._result = {}

    def evaluate_test_result(self):
        self._classifier.load(self._picked_uuid)
        validation_error = self._classifier.get_error(self._validation_data["data"], self._validation_data["labels"])
        test_error = self._classifier.get_error(self._test_data["data"], self._test_data["labels"])

        self._result = {
            "uuid": self._picked_uuid,
            "test_error": test_error,
            "validation_error": validation_error,
            "difference": abs(test_error - validation_error)
        }

    def generate_test_report(self):
        read_result, file_content = JsonReader.read_json_file(os.getenv("HYPER_PARAMS_FILE_PATH"))
        if not read_result:
            return
        self._result["tolerance"] = file_content["validation-tolerance"]

        test_report_generator = TestReportGenerator(self._result)
        test_report_generator.generate_test_report()

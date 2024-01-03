import os
import math
from itertools import product
from operator import itemgetter

from model.classifier import Classifier
from model.classifier_configuration import ClassifierConfiguration
from utils.json_reader import JsonReader
from model.dataset import Dataset
from generator.validation_report_generator import ValidationReportGenerator

class ValidationManager:

    def __init__(self):
        self._classifier = Classifier()
        self._train_data = Dataset.get_data("train")
        self._validation_data = Dataset.get_data("validation")
        self._best_classifiers = []

    def get_setting_list(self):
        read_result , file_content = JsonReader.read_json_file(os.getenv("HYPER_PARAMS_FILE_PATH"))
        if not read_result:
            return
        iterations_number = file_content["iterations-number"]
        overfitting_threshold = file_content["overfitting-threshold"]
        hidden_layer_size_range = file_content["hidden-layer-size-range"]
        hidden_neuron_range = file_content["hidden-neuron-per-layer-range"]

        exponent = int(math.log2(hidden_neuron_range[1]))
        layer_number = hidden_layer_size_range[1]
        hidden_layer_sizes_options = []
        neuron_options = [2**i for i in range(exponent, 2, -1)]

        for n_layers in range(1, layer_number):
            layer_combinations = list(product(neuron_options, repeat=n_layers))
            for combination in layer_combinations:
                is_decreasing = all(
                    combination[i] >= combination[i + 1] for i in range(len(combination) - 1)
                )
                if is_decreasing:
                    hidden_layer_sizes_options.append(combination)

        return hidden_layer_sizes_options , iterations_number , overfitting_threshold

    def get_best_classifier(self):
        grid_search_result, iterations_number, overfitting_threshold = self.get_setting_list()
        for index, setting in enumerate(grid_search_result):
            config = ClassifierConfiguration(iterations_number , setting)
            self._classifier.update_configuration(config)
            self._classifier.train_classifier(self._train_data["data"] , self._train_data["labels"])

            train_error = self._classifier.get_error(
                                self._train_data["data"],
                                self._train_data["labels"]
                            )

            validation_error = self._classifier.get_error(
                                    self._validation_data["data"],
                                    self._validation_data["labels"]
                                )

            if (validation_error - train_error) > overfitting_threshold:
                continue

            self._classifier.save("NN" + str(index))

            neurons = 0
            for elem in setting:
                neurons += elem

            model = {
                "uuid" : "NN" + str(index),
                "train_error" : train_error,
                "validation_error" : validation_error,
                "layers" : len(setting),
                "neurons": neurons,
                "hidden_layers_structure" : setting,
                "error_difference" : abs(validation_error - train_error),
                "overfitting_threshold": overfitting_threshold
            }

            self._best_classifiers.append(model)
            self._best_classifiers = sorted(
                self._best_classifiers,
                key=itemgetter('validation_error')
            )

            if len(self._best_classifiers) > 5:
                self._best_classifiers.pop(5)
        print("[DEBUG] BEST 5 CLASS : " , self._best_classifiers)

    def evaluate_validation_result(self):
        report_generator = ValidationReportGenerator(self._best_classifiers)
        report_generator.generate_report()

    def clear_classifier_directory(self , uuid):
        classifier_file_name = uuid + ".joblib"
        for classifier in os.listdir(os.getenv("CLASSIFIER_DIRECTORY_PATH")):
            if classifier != classifier_file_name:
                os.remove(os.getenv("CLASSIFIER_DIRECTORY_PATH") + classifier)

    def pick_classifier(self, uuid):
        read_result, file_content = JsonReader.read_json_file(os.getenv("BEST_CLASSIFIER_FILE_PATH"))
        if not read_result:
            return

        for classifier in file_content:
            if classifier["uuid"] == uuid:
                JsonReader.write_json_file(os.getenv("PICKED_CLASSIFIER_FILE_PATH") , classifier)

        self.clear_classifier_directory(uuid)

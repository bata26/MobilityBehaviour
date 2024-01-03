import warnings
import os
import pandas as pd
import joblib

from sklearn.neural_network import MLPClassifier
from sklearn.exceptions import ConvergenceWarning, DataConversionWarning
from utils.json_reader import JsonReader
from model.classifier_configuration import ClassifierConfiguration

class Classifier:

    def __init__(self):
        self._classifier = MLPClassifier()
        self._configuration = ClassifierConfiguration()

        # remove the training warnings
        warnings.filterwarnings("ignore", category=ConvergenceWarning)
        warnings.filterwarnings("ignore", category=DataConversionWarning)

    def train_classifier(self, training_data, training_labels):
        training_data = pd.DataFrame(training_data)
        self._classifier.fit(training_data, training_labels)

    def get_error(self, data, labels):
        data = pd.DataFrame(data)
        return self._classifier.score(data, labels)

    def get_losses(self):
        return self._classifier.loss_curve_

    def update_configuration(self, configuration):
        if (
                (
                    self._configuration is not  None
                    and  self._configuration.iterations_number != configuration.iterations_number
                )
                or self._configuration is None
            ):
            print("[DEBUG] Update config file")
            JsonReader.update_json_file(
                os.getenv("HYPER_PARAMS_FILE_PATH"),
                "iterations-number" , 
                configuration.iterations_number
            )
        self._configuration = configuration
        self._classifier.set_params(**configuration.to_dict())

    def save(self , uuid):
        file_path = os.getenv("CLASSIFIER_DIRECTORY_PATH") + uuid + ".joblib"
        joblib.dump(self._classifier, file_path)

    def load(self, uuid):
        file_path = file_path = os.getenv("CLASSIFIER_DIRECTORY_PATH") + uuid + ".joblib"
        self._classifier = joblib.load(file_path)

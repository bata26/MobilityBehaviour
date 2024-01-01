import warnings
import os
import joblib

import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.exceptions import ConvergenceWarning, DataConversionWarning

class Classifier:
    _instance = None

    def __init__(self):
        self._classifier = MLPClassifier()

        # remove the training warnings
        warnings.filterwarnings("ignore", category=ConvergenceWarning)
        warnings.filterwarnings("ignore", category=DataConversionWarning)

    def load(self):
        file_path = os.getenv("CLASSIFIER_FILE_PATH")
        self._classifier = joblib.load(file_path)

    def predict_label(self , net_input):
        print("[DEBUG] input " , net_input)
        res = self._classifier.predict(pd.DataFrame(net_input))
        print("[DEBUG] predict result: " , res)
        return res

    @staticmethod
    def get_instance():
        if Classifier._instance is None:
            Classifier._instance = Classifier()
        return Classifier._instance

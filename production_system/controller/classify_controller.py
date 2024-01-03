from model.classifier import Classifier

class ClassifyController:
    labels_int_to_human = {
        "0.0" : "Regular",
        "1.0" : "Anomalous"
    }

    def __init__(self , prepared_session):
        self._prepared_session = prepared_session
        self._classifier = Classifier.get_instance()

    def classify(self):
        classify_raw_result = self._classifier.predict_label(self._prepared_session.to_dataset())
        #human_label = self.labels_int_to_human[str(classify_raw_result[0])]
        self._prepared_session.add_human_output(classify_raw_result[0])
        return self._prepared_session.to_json()

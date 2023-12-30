from model.classifier import Classifier

class DeployController:

    def __init__(self):
        self._classifier = Classifier.get_instance()

    def deploy_classifier(self):
        self._classifier.load()

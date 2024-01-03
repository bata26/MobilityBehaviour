from model.validation_manager import ValidationManager
class ValidationController:

    def __init__(self):
        print("[INFO] Set Hyperparameters")
        self._manager = ValidationManager()

    def validate_classifier(self):
        self._manager.get_best_classifier()

    def generate_validation_report(self):
        self._manager.evaluate_validation_result()

    def select_classifier(self , uuid):
        self._manager.pick_classifier(uuid)

from model.training_manager import TrainingManager
from controller.generator.learning_report_generator import LearningReportGenerator

class TrainingController:
    def __init__(self):
        print("[INFO] Set Average Hyperparameters")
        self._manager = TrainingManager()
    def set_average_hyperparameters(self):
        self._manager.set_average_hyperparameters()
    def update_iterations_number(self, iterations):
        self._manager.update_iterations_number(iterations)
    def start_training(self):
        print("[INFO] Starting trainig..")
        self._manager.train_classifier( )
        print("[INFO] Ended training")

    def generate_learning_report(self):
        LearningReportGenerator(self._manager.get_classifier_losses())

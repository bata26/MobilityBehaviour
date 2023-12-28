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

        #training_error = self.classifier.get_error(data=self.train_data.data,
        #                                            labels=self.train_data.labels)
        #EarlyTrainingReportGenerator().generate_report(training_parameter=training_parameters,
        #                                                training_error=training_error,
        #                                                testing=testing)
#
        ## generate the gradient descent plot
        #GradientDescentPlotGenerator().generate_plot(losses=self.mental_command_classifier.get_losses())
        LearningReportGenerator(self._manager.get_classifier_losses())

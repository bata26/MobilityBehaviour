from model.learning_report import LearningReport
class LearningReportGenerator():

    def __init__(self, losses):
        LearningReport(losses).show_plot()

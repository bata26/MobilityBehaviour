import os
from model.report import Report

class ValidationReportGenerator:

    def __init__(self, best_classifiers):
        self._report = Report(best_classifiers)

    def generate_report(self):
        print("[INFO] Generate json report")
        self._report.generate_json(os.getenv("BEST_CLASSIFIER_FILE_PATH"))
        print("[INFO] Json report generated")
        print("[INFO] Generate csv report")
        self._report.generate_csv(os.getenv("BEST_CLASSIFIER_CSV_FILE_PATH"))
        print("[INFO] Csv report generated")
    
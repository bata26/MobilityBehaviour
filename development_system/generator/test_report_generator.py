import os
from model.report import Report

class TestReportGenerator:

    def __init__(self, data):
        self._report = Report([data])

    def generate_test_report(self):
        self._report.generate_json(os.getenv("TEST_RESULT_FILE_PATH"))
        self._report.generate_csv(os.getenv("TEST_RESULT_CSV_FILE_PATH"))

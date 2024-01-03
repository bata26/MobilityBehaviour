from model.test_manager import TestManager

class TestController:

    def __init__(self):
        self._manager = TestManager()

    def evaluate_test_result(self):
        self._manager.evaluate_test_result()

    def generate_test_report(self):
        self._manager.generate_test_report()

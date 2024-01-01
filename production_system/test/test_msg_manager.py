import os
import pytest
from flask import Flask
from flask_testing import LiveServerTestCase
import sys
sys.path.insert(0, r'../../production_system')
from model.msg_manager import MessageManager  # Replace 'your_module_name' with the module where MessageManager is defined

@pytest.fixture
def sample_session():
    # Sample session data for testing
    return {
        "_id": "1",
        "label": "Sample Label",
        "features": {
            "maximum_pressure_ts": 10,
            "minimum_pressure_ts": 5,
            "median_pressure_ts": 7,
            "mean_absolute_deviation_pressure_ts": 2,
            "activity_and_small_scatter": 3,
            "environment_and_small_scatter": 3
        }
    }

class TestMessageManager(LiveServerTestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def set_up(self):
        self.message_manager = MessageManager.get_instance()
        self.client = self.app.test_client()

    def test_deploy_endpoint(self):
        with open('test_classifier_file', 'rb') as file:
            data = {'file': (file, 'test_classifier.txt')}
            response = self.client.post('/deploy', data=data)

        assert response.status_code == 200

    def test_prepared_session_endpoint(self, sample_session):
        response = self.client.post('/preparedsession', json=sample_session)

        assert response.status_code == 200

    def test_send_post_request(self):
        # Test send_post_request function with different destinations
        dests = ["EVALUATION", "CLIENT", "UNKNOWN_DEST"]
        for dest in dests:
            # Simulate sending data to different destinations
            data = {'key': 'value'}
            self.message_manager.send_post_request(dest, data)
            # Add assertions to verify expected behavior based on destination

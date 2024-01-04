import sys
import pytest
import random
from dotenv import load_dotenv

sys.path.insert(0, r'../../evaluation_system')
from model.msg_manager import MessageManager

load_dotenv()


@pytest.fixture
def message_manager():
    return MessageManager.get_instance()


def send_labels(message_manager, endpoint, num_labels):
    labels = [{"uuid": str(i), "label": random.choice(["Anomalous", "Regular"])} for i in range(num_labels)]
    for label in labels:
        response = message_manager.get_app().test_client().post(f"/{endpoint}", json=label)
        assert response.status_code == 200


def test_system_flow(message_manager):
    send_labels(message_manager, "expertLabels", 5)
    send_labels(message_manager, "classifierLabels", 5)

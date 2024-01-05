import sys
import pytest
from dotenv import load_dotenv
sys.path.insert(0, r'../../development_system')
from model.msg_manager import MessageManager
load_dotenv()

@pytest.fixture
def message_manager():
    return MessageManager.get_instance()
# JSON BODY
@pytest.fixture
def json_body():
    return {
        "train": {
            "number_of_samples": 2,
            "features": [
            {
                "maximum_pressure_ts": 0.0,
                "minimum_pressure_ts": 0.0,
                "median_pressure_ts": 0.0,
                "mean_absolute_deviation_pressure_ts": 0.0,
                "activity_and_small_scatter": 0.0,
                "environment_and_small_scatter": 0.0,
                "label": "Regular"
            },
            {
                "maximum_pressure_ts": 0.0,
                "minimum_pressure_ts": 0.0,
                "median_pressure_ts": 0.0,
                "mean_absolute_deviation_pressure_ts": 0.0,
                "activity_and_small_scatter": 0.0,
                "environment_and_small_scatter": 0.0,
                "label": "Regular"
            }
            ]
        },
        "validation": {
            "number_of_samples": 2,
            "features": [
            {
                "maximum_pressure_ts": 0.0,
                "minimum_pressure_ts": 0.0,
                "median_pressure_ts": 0.0,
                "mean_absolute_deviation_pressure_ts": 0.0,
                "activity_and_small_scatter": 0.0,
                "environment_and_small_scatter": 0.0,
                "label": "Regular"
            },
            {
                "maximum_pressure_ts": 0.0,
                "minimum_pressure_ts": 0.0,
                "median_pressure_ts": 0.0,
                "mean_absolute_deviation_pressure_ts": 0.0,
                "activity_and_small_scatter": 0.0,
                "environment_and_small_scatter": 0.0,
                "label": "Regular"
            }
            ]
        },
        "test": {
            "number_of_samples": 2,
            "features": [
            {
                "maximum_pressure_ts": 0.0,
                "minimum_pressure_ts": 0.0,
                "median_pressure_ts": 0.0,
                "mean_absolute_deviation_pressure_ts": 0.0,
                "activity_and_small_scatter": 0.0,
                "environment_and_small_scatter": 0.0,
                "label": "Regular"
            },
            {
                "maximum_pressure_ts": 0.0,
                "minimum_pressure_ts": 0.0,
                "median_pressure_ts": 0.0,
                "mean_absolute_deviation_pressure_ts": 0.0,
                "activity_and_small_scatter": 0.0,
                "environment_and_small_scatter": 0.0,
                "label": "Regular"
            }
            ]
        }
        }

def test_send_request(message_manager, json_body):
    res = message_manager.get_app().test_client().post("/senddata" , json = json_body)
    assert res.status_code == 200


def test_get_instance(message_manager):
    assert message_manager is not None
    assert isinstance(message_manager, MessageManager)
    assert MessageManager.get_instance().get_app() == message_manager.get_app()

def test_send_to_main(message_manager):
    dataset = {"key": "value"}
    message_manager.send_to_main(dataset)
    assert not message_manager.get_queue().empty()

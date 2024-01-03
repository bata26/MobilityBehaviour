import sys
import pytest
from dotenv import load_dotenv
sys.path.insert(0, r'../../production_system')
from model.prepared_session import PreparedSession
load_dotenv()

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

def test_to_dataset(sample_session):
    prepared_session = PreparedSession(sample_session)
    dataset = prepared_session.to_dataset()
    assert len(dataset) == 1
    assert dataset[0]["maximum_pressure_ts"] == sample_session["features"]["maximum_pressure_ts"]
    assert dataset[0]["minimum_pressure_ts"] == sample_session["features"]["minimum_pressure_ts"]
    assert dataset[0]["median_pressure_ts"] == sample_session["features"]["median_pressure_ts"]
    assert dataset[0]["mean_absolute_deviation_pressure_ts"] == sample_session["features"]["mean_absolute_deviation_pressure_ts"]
    assert dataset[0]["activity"] == sample_session["features"]["activity_and_small_scatter"]
    assert dataset[0]["environment"] == sample_session["features"]["environment_and_small_scatter"]

def test_add_human_output(sample_session):
    prepared_session = PreparedSession(sample_session)
    assert prepared_session.human_output == ""

    output_text = "Test output"
    prepared_session.add_human_output(output_text)
    assert prepared_session.human_output == output_text

def test_to_json(sample_session):
    prepared_session = PreparedSession(sample_session)
    prepared_session.add_human_output("Test output")
    json_data = prepared_session.to_json()
    assert json_data["uuid"] == sample_session["_id"]
    assert json_data["label"] == prepared_session.human_output

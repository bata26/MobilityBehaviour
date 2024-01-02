import sys
import pytest
from dotenv import load_dotenv
sys.path.insert(0, r'../../development_system')
from model.dataset import Dataset
load_dotenv()

# DATASET OBJECT
@pytest.fixture
def dataset():
    return {
        "data": {
            "maximum_pressure_ts": [0.0, 0.0],
            "minimum_pressure_ts": [0.0, 0.0],
            "median_pressure_ts": [0.0, 0.0],
            "mean_absolute_deviation_pressure_ts": [0.0, 0.0],
            "activity": [0.0, 0.0],
            "environment": [0.0, 0.0],
        },
        "labels": [0.0, 0.0],
    }

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
                "label": 0.0
            },
            {
                "maximum_pressure_ts": 0.0,
                "minimum_pressure_ts": 0.0,
                "median_pressure_ts": 0.0,
                "mean_absolute_deviation_pressure_ts": 0.0,
                "activity_and_small_scatter": 0.0,
                "environment_and_small_scatter": 0.0,
                "label": 0.0
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
                "label": 0.0
            },
            {
                "maximum_pressure_ts": 0.0,
                "minimum_pressure_ts": 0.0,
                "median_pressure_ts": 0.0,
                "mean_absolute_deviation_pressure_ts": 0.0,
                "activity_and_small_scatter": 0.0,
                "environment_and_small_scatter": 0.0,
                "label": 0.0
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
                "label": 0.0
            },
            {
                "maximum_pressure_ts": 0.0,
                "minimum_pressure_ts": 0.0,
                "median_pressure_ts": 0.0,
                "mean_absolute_deviation_pressure_ts": 0.0,
                "activity_and_small_scatter": 0.0,
                "environment_and_small_scatter": 0.0,
                "label": 0.0
            }
            ]
        }
        }



def test_dataset(json_body , dataset):
    Dataset.set_data(json_body)
    assert Dataset.get_data("train") == dataset
    assert Dataset.get_data("validation") == dataset
    assert Dataset.get_data("test") == dataset
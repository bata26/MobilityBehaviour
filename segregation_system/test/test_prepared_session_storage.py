import sys
import pytest
sys.path.insert(0, r'../../segregation_system')
from src.prepared_session_storage import PreparedSessionStorage

@pytest.fixture
def test_session():
    return {
    "_id" : "1",
    "calendar" : "shopping",
    "environment" : "slippery",
    "label" : "Regular",
    "features" : 
        {
            "maximum_pressure_ts" : 5.0,
            "minimum_pressure_ts" : 4.0,
            "median_pressure_ts" : 3.0,
            "mean_absolute_deviation_pressure_ts" : 6.0,
            "activity_and_small_scatter" : 1.0,
            "environment_and_small_scatter" : 2.0
        }
    }

@pytest.fixture
def test_config():
    return{
        "stage": "store",
        "segregation_system_ip": "0.0.0.0",
        "segregation_system_port": "6000",
        "development_system_ip": "10.8.0.2",
        "development_system_port": "6000",
        "preparation_system_ip": "10.8.0.6",
        "preparation_system_port": "5000",
        "db_name": "test_segregation.db",
        "max_sessions": 350,
        "train_set_size": 0.7,
        "validation_set_size": 0.2,
        "test_set_size": 0.1
    }

@pytest.fixture
def test_schema():
    return {
    "type": "object",
    "properties": {
      "_id": {"type": "string"},
      "calendar": {"type": "string"},
      "environment": {"type": "string"},
      "label": {"type": "string"},
      "features": 
      {
        "type": "object",
        "properties" : {
          "maximum_pressure_ts": {"type": "number"},
          "minimum_pressure_ts": {"type": "number"},
          "median_pressure_ts": {"type": "number"},
          "mean_absolute_deviation_pressure_ts": {"type": "number"},
          "activity_and_small_scatter": {"type": "number"},
          "environment_and_small_scatter": {"type": "number"}
        }
      }
    },
    "required": ["_id", "calendar", "environment", "label", "features"]
  }

def test_increment_session_counter(test_config):
    collector = PreparedSessionStorage(test_config)
    collector.increment_session_counter()
    assert collector.prepared_session_counter == 1

def test_check_max_sessions(test_config):
    collector = PreparedSessionStorage(test_config)
    max_sessions = collector.segregation_system_config['max_sessions']
    assert max_sessions == test_config['max_sessions']

def test_validate_prepared_session(test_config, test_session):
    collector = PreparedSessionStorage(test_config)
    result = collector.validate_prepared_session(test_session)
    assert result == True

def test_load_dataset(test_config):
    collector = PreparedSessionStorage(test_config)
    result = collector.load_dataset()
    assert len(result) == 0

def test_store_prepared_session(test_session, test_config):
    collector = PreparedSessionStorage(test_config)
    result = collector.store_prepared_session(test_session)
    assert result is True

def test_empty_db(test_config):
    collector = PreparedSessionStorage(test_config)
    result = collector.empty_db()
    assert result is True

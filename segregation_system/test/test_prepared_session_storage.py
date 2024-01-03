import os
import sys
import json
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

def test_increment_session_counter():
    config_path = os.path.join(os.path.abspath('.'), 'data', 'test_segregation_system_config.json')
    collector = PreparedSessionStorage(config_path)
    counter = collector.increment_session_counter()
    assert counter == counter + 1

def test_check_max_sessions():
    config_path = os.path.join(os.path.abspath('.'), 'data', 'test_segregation_system_config.json')
    with open(config_path) as f:
        config = json.load(f)
    collector = PreparedSessionStorage(config_path)
    max_sessions = collector.segregation_system_config['max_sessions']
    assert max_sessions == config['max_sessions']

def test_validate_prepared_session():
    config_path = os.path.join(os.path.abspath('.'), 'data', 'test_segregation_system_config.json')
    schema_path = os.path.join(os.path.abspath('..'), 'schemas', 'prepared_session_schema.json')
    with open(schema_path) as f1:
        schema = json.load(f1)
    collector = PreparedSessionStorage(config_path)
    result = collector.validate_prepared_session(test_session, schema)
    assert result == True

def test_load_dataset():
    config_path = os.path.join(os.path.abspath('.'), 'data', 'test_segregation_system_config.json')
    with open(config_path) as f1:
        config = json.load(f1)
    collector = PreparedSessionStorage(config)
    result = collector.load_dataset()
    assert len(result) == 40

def test_store_prepared_session(test_session):
    config_path = os.path.join(os.path.abspath('.'), 'data', 'test_segregation_system_config.json')
    with open(config_path) as f1:
        config = json.load(f1)
    collector = PreparedSessionStorage(config)
    result = collector.store_prepared_session(test_session)
    assert result is True

def test_empty_db():
    config_path = os.path.join(os.path.abspath('.'), 'data', 'test_segregation_system_config.json')
    with open(config_path) as f1:
        config = json.load(f1)
    collector = PreparedSessionStorage(config)
    result = collector.empty_db()
    assert result is True

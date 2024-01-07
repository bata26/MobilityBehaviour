import sys
import os
import tempfile
import json
import pytest
sys.path.insert(0, r'..')
from src.ingestion_system_configuration import IngestionSystemConfiguration


# Fixture to create a temporary JSON schema file for testing
@pytest.fixture
def temp_config_schema_file():
    schema = {
        "type": "object",
        "properties": {
            "operative_mode": {
                "type": "string",
                "enum": ["development", "production"]
            },
            "preparation_system_ip": {
                "type": "string"
            },
            "preparation_system_port": {
                "type": "integer"
            },
            "evaluation_system_ip": {
                "type": "string"
            },
            "evaluation_system_port": {
                "type": "integer"
            },
            "production_window": {
                "type": "integer"
            },
            "evaluation_window": {
                "type": "integer"
            },
            "missing_samples_threshold": {
                "type": "integer"
            },
            "db_name": {
                "type": "string"
            }
        },
        "required": [
            "operative_mode",
            "preparation_system_ip",
            "preparation_system_port",
            "evaluation_system_ip",
            "evaluation_system_port",
            "production_window",
            "evaluation_window",
            "missing_samples_threshold",
            "db_name"
            ]
    }

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_schema_file:
        json.dump(schema, temp_schema_file)
        temp_schema_file.flush()
        yield temp_schema_file.name
    os.remove(temp_schema_file.name)

# Fixture to create a temporary JSON file for testing
@pytest.fixture
def temp_config_file():
    content = {
        "operative_mode" : "development",
        "preparation_system_ip" : "127.0.0.1",
        "preparation_system_port" : 5000,
        "evaluation_system_ip": "10.8.0.7",
        "evaluation_system_port": 6000,
        "production_window": 5,
        "evaluation_window": 5,
        "missing_samples_threshold": 1,
        "db_name":"mobility.db"
    }
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        json.dump(content, temp_file)
        temp_file.flush()
        yield temp_file.name
    os.remove(temp_file.name)

def test_ingestion_system_configuration(temp_config_file, temp_config_schema_file):
    IngestionSystemConfiguration(temp_config_file, temp_config_schema_file)
    assert True

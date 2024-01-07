import sys
import os
import tempfile
import json
import pytest
sys.path.insert(0, r'..')
from utility.json_handler import JsonHandler

# Fixture to create a temporary JSON file for testing
@pytest.fixture
def temp_json():
    label_content = {
        "uuid": "_id",
        "pressure_detected": "Regular"
    }
    return label_content

@pytest.fixture
def temp_json_schema():
    schema = {
        "type": "object",
        "properties": {
            "pressure_detected": {
                "type": "string",
                "enum": ["Anomalous", "Regular"]
            },
            "uuid": {
                "type": "string"
            }
        },
        "required": ["pressure_detected", "uuid"]
    }
    return schema

# Fixture to create a temporary JSON schema file for testing
@pytest.fixture
def temp_json_schema_file():
    schema = {
        "type": "object",
        "properties": {
            "pressure_detected": {
                "type": "string",
                "enum": ["Anomalous", "Regular"]
            },
            "uuid": {
                "type": "string"
            }
        },
        "required": ["pressure_detected", "uuid"]
    }

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_schema_file:
        json.dump(schema, temp_schema_file)
        temp_schema_file.flush()
        yield temp_schema_file.name
    os.remove(temp_schema_file.name)

# Fixture to create a temporary JSON file for testing
@pytest.fixture
def temp_json_file():
    content = {
        "key1": "value1",
        "key2": "value2"
    }
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        json.dump(content, temp_file)
        temp_file.flush()
        yield temp_file.name
    os.remove(temp_file.name)

def test_load_json_file(temp_json_file):
    json_handler = JsonHandler()
    file_content = json_handler.load_json(temp_json_file)
    assert file_content == {"key1": "value1", "key2": "value2"}

def test_validate_json_data_file(temp_json, temp_json_schema_file):
    json_handler = JsonHandler()
    success = json_handler.validate_json_data_file \
        (json_data=temp_json, schema_path=temp_json_schema_file)
    assert success is True

def test_validate_json(temp_json, temp_json_schema):
    json_handler = JsonHandler()
    success = json_handler.validate_json(json_data=temp_json, schema=temp_json_schema)
    assert success is True

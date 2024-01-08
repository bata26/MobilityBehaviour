import sys
import os
import tempfile
import json
import pytest
sys.path.insert(0, r'..')
from utility.json_handler import JsonHandler



# Fixture to create a temporary JSON file for testing
@pytest.fixture
def test_raw_session_json():
    return {
        "key1": "value1",
        "key2": "value2"
    }

@pytest.fixture
def test_json_schema():
    schema = {
        "type": "object",
        "properties": {
            "key1": {
                "type": "string"
            },
            "key2": {
                "type": "string",
            }
        },
        "required": ["key1", "key2"]
    }
    return schema

# Fixture to create a temporary JSON schema file for testing
@pytest.fixture
def test_json_schema_file():
    schema = {
        "type": "object",
        "properties": {
            "key1": {
                "type": "string"
            },
            "key2": {
                "type": "string",
            }
        },
        "required": ["key1", "key2"]
    }
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_schema_file:
        json.dump(schema, temp_schema_file)
        temp_schema_file.flush()
        yield temp_schema_file.name
    os.remove(temp_schema_file.name)

# Fixture to create a temporary JSON file for testing
@pytest.fixture
def test_raw_session_file():
    content = {
        "key1": "value1",
        "key2": "value2"
    }
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        json.dump(content, temp_file)
        temp_file.flush()
        yield temp_file.name
    os.remove(temp_file.name)

def test_load_json_file(test_raw_session_file):
    json_handler = JsonHandler()
    file_content = json_handler.load_json(test_raw_session_file)
    assert file_content == {
        "key1": "value1",
        "key2": "value2"
    }

def test_validate_json_data_file(test_raw_session_json, test_json_schema_file):
    json_handler = JsonHandler()
    success = json_handler.validate_json_data_file(json_data=test_raw_session_json, \
                                                    schema_path=test_json_schema_file)
    assert success is True

def test_validate_json(test_raw_session_json, test_json_schema):
    json_handler = JsonHandler()
    success = json_handler.validate_json(json_data=test_raw_session_json, schema=test_json_schema)
    assert success is True

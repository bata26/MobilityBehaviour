import sys
import os
import tempfile
import json
import pytest
from dotenv import load_dotenv
sys.path.insert(0, r'../../development_system')
from utils.json_reader import JsonReader
load_dotenv()

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

def test_read_json_file(temp_json_file):
    success, file_content = JsonReader.read_json_file(temp_json_file)
    assert success is True
    assert file_content == {"key1": "value1", "key2": "value2"}

def test_read_json_file_nonexistent():
    non_existent_file = "non_existent_file.json"
    success, file_content = JsonReader.read_json_file(non_existent_file)
    assert success is False
    assert file_content is None

def test_update_json_file(temp_json_file):
    success = JsonReader.update_json_file(temp_json_file, "key3", "value3")
    assert success is True

    _, file_content = JsonReader.read_json_file(temp_json_file)
    assert file_content == {"key1": "value1", "key2": "value2", "key3": "value3"}

def test_update_json_file_error():
    error_file = "error_file.json" 
    success = JsonReader.update_json_file(error_file, "key3", "value3")
    assert success is False

def test_write_json_file(temp_json_file):
    new_content = {"key1": "updated_value1", "key4": "value4"}
    success = JsonReader.write_json_file(temp_json_file, new_content)
    assert success is True

    _, file_content = JsonReader.read_json_file(temp_json_file)
    assert file_content == new_content

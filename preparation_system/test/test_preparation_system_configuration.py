import sys
import os
import tempfile
import json
import pytest
sys.path.insert(0, r'..')
from src.preparation_system_configuration import PreparationSystemConfiguration


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
    "segregation_system_ip": {
      "type": "string"
    },
    "segregation_system_port": {
      "type": "integer"
    },
    "production_system_ip": {
      "type": "string"
    },
    "production_system_port": {
      "type": "integer"
    },
    "max_value": {
      "type": "number"
    },
    "min_value": {
      "type": "number"
    },
    "features": {
      "type": "object",
      "properties": {
        "environment": {
          "type": "object",
          "properties": {
            "slippery": {
              "type": "integer"
            },
            "plain": {
              "type": "integer"
            },
            "slope": {
              "type": "integer"
            },
            "house": {
              "type": "integer"
            },
            "track": {
              "type": "integer"
            }
          },
          "required": [
            "slippery",
            "plain",
            "slope",
            "house",
            "track"
          ]
        },
        "calendar": {
          "type": "object",
          "properties": {
            "shopping": {
              "type": "integer"
            },
            "sport": {
              "type": "integer"
            },
            "cooking": {
              "type": "integer"
            },
            "gaming": {
              "type": "integer"
            }
          },
          "required": [
            "shopping",
            "sport",
            "cooking",
            "gaming"
          ]
        }     
      }
    }
  },
  "required": [
  "operative_mode",
  "segregation_system_ip",
  "segregation_system_port",
  "production_system_ip",
  "production_system_port",
  "min_value",
  "max_value",
  "features"
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
  "operative_mode": "development",
  "segregation_system_ip": "10.8.0.3",
  "segregation_system_port": 6000,
  "production_system_ip": "10.8.0.2",
  "production_system_port": 6001,
  "max_value": 3.5,
  "min_value": 0,
  "features": {
    "environment": {"slippery": 1, "plain": 2, "slope": 3, "house":4, "track":5 },
    "calendar": {"shopping":1, "sport":2, "cooking":3, "gaming":4}
  }
}

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        json.dump(content, temp_file)
        temp_file.flush()
        yield temp_file.name
    os.remove(temp_file.name)

def test_ingestion_system_configuration(temp_config_file, temp_config_schema_file):
    configuration = PreparationSystemConfiguration(temp_config_file, temp_config_schema_file)
    assert True

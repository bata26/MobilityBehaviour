import sys
from jsonschema import ValidationError
import pytest
from dotenv import load_dotenv
sys.path.insert(0, r'../../development_system')
from model.json_validator import JsonValidator
load_dotenv()

def test_validate_schemas_with_exception():
    print("[TEST] Validate json files with wrong json file")
    with pytest.raises(ValidationError):
        JsonValidator.validate_schemas()

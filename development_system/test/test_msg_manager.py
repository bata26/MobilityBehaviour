import os
import pytest
import sys
from jsonschema import ValidationError
import pytest
from dotenv import load_dotenv
sys.path.insert(0, r'../../development_system')
from model.msg_manager import MessageManager  
load_dotenv()
# Replace 'your_module_name' with the module where MessageManager is defined

@pytest.fixture
def message_manager():
    return MessageManager.get_instance()

def test_get_instance(message_manager):
    assert message_manager is not None
    assert isinstance(message_manager, MessageManager)
    assert MessageManager.get_instance().get_app() == message_manager.get_app()

def test_send_to_main(message_manager):
    dataset = {"key": "value"}
    message_manager.send_to_main(dataset)
    assert not message_manager.get_queue().empty()

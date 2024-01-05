import os
import sys
import pytest
from dotenv import load_dotenv
sys.path.insert(0, r'../../development_system')
from model.dataset import Dataset
from utils.json_reader import JsonReader
from model.msg_manager import MessageManager
from controller.development_system import DevelopmentSystem

load_dotenv()

@pytest.fixture
def dataset():
    print("prima fixture")
    res , file_content = JsonReader.read_json_file("./json/request-example.json")
    return Dataset.set_data(file_content)

@pytest.fixture
def system():
    print("seconda fixture")
    return DevelopmentSystem()

def test_chain(dataset , system):
    system.update_stage("set_avg_hyp")
    system.run(productivity=True)

    # Learning phase
    assert os.path.isfile("./images/learning_plot.png") is True

    # Validation phase
    assert os.path.isfile("./csv/best-classifiers.csv") is True
    assert os.path.isfile("./json/best-classifiers.json") is True

    # Test Phase
    assert os.path.isfile("./json/test-result.json") is True
    assert os.path.isfile("./csv/test-result.csv") is True

    # Picked classifier
    assert os.path.isfile("./json/picked-classifier.json") is True
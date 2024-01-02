import os
import sys
import pytest
from dotenv import load_dotenv
sys.path.insert(0, r'../../development_system')
from model.report import Report
load_dotenv()

@pytest.fixture
def csv_file_path():
    return "./csv/test-file.csv"

@pytest.fixture
def json_file_path():
    return "./json/test-file.json"

@pytest.fixture
def data():
    return [{
        "key" : "value"
    },
    {
        "key" : "value"
    },
    {
        "key" : "value"
    },
    {
        "key" : "value"
    }]


def test_json_file(data, json_file_path):
    report = Report(data)
    report.generate_json(json_file_path)
    assert os.path.isfile(json_file_path) is True

def test_csv_file(data, csv_file_path):
    report = Report(data)
    report.generate_csv(csv_file_path)
    assert os.path.isfile(csv_file_path) is True

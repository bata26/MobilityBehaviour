import os
import sys
import pytest
import pandas as pd
from jsonschema import validate
import json

sys.path.insert(0, r'../../evaluation_system')
from model.evaluation_report_generator import EvaluationReportGenerator
from model.system_configuration import SystemConfiguration
from utils.json_reader import JsonReader


@pytest.fixture
def sample_label_df():
    # Create a sample label DataFrame for testing
    data = {
        'expertLabel': ['Normal', 'Anomalous', 'Normal', 'Anomalous', 'Normal'],
        'classifierLabel': ['Normal', 'Anomalous', 'Anomalous', 'Anomalous', 'Normal']
    }
    return pd.DataFrame(data)


def test_generate_report(sample_label_df):
    # Create an instance of EvaluationReportGenerator

    config = SystemConfiguration("../data/system_configuration.json")

    report_generator = EvaluationReportGenerator(config)

    # Generate the report using the sample label DataFrame
    report_generator.generate_report(sample_label_df)

    # Check if the report JSON file has been created
    report_path = os.path.join(os.path.abspath('.'), 'data', 'report.json')
    assert os.path.isfile(report_path)

    # Read the generated report to check its content
    with open(report_path, 'r', encoding='UTF-8') as file:
        report_content = file.read()

    # Validate the generated report against the expected schema
    read_result, schema_content = JsonReader.read_json_file("./data/evaluation_report_schema.json")
    report_data = json.loads(report_content)

    try:
        validate(instance=report_data, schema=schema_content)
        # Validation passed without raising an exception
        assert True
    except Exception as e:
        # Validation failed, print details of the validation error
        print(f"Validation error: {e}")
        assert False

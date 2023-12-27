import os
import sys
import json
from jsonschema import validate, ValidationError
from json_io import JsonIO
from label_storage import LabelStorage 
from evaluation_report_generator import EvaluationReportGenerator

class EvaluationSystem:

    def __init__(self):
        self.evaluation_system_config = None

    def import_config(self):
        config_path = os.path.join(os.path.abspath('.'), 'data', 'evaluation_system_config.json')
        schema_path = os.path.join(os.path.abspath('.'), 'schemas',
                                   'evaluation_system_config_schema.json')

        try:
            with open(config_path) as file:
                evaluation_system_config = json.load(file)

            with open(schema_path) as file:
                evaluation_system_config_schema = json.load(file)

            validate(evaluation_system_config, evaluation_system_config_schema)

        except FileNotFoundError:
            print('Failed to open evaluation_system_config.json')
            print('Shutdown')
            sys.exit(1)

        except ValidationError:
            print('Config validation failed')
            print('Shutdown')
            sys.exit(1)

        self.evaluation_system_config = evaluation_system_config

    def save_config(self):
        config_path = os.path.join(os.path.abspath('.'), 'data', 'evaluation_system_config.json')
        try:
            with open(config_path, "w") as file:
                json.dump(self.evaluation_system_config, file, indent=4)
        except Exception as e:
            print(e)
            print('Failure to save evaluation_system_config.json')
            return False
        return True

    def run(self):
        self.import_config()

        # Handle the flow

        return True

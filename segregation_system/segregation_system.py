import os
import sys
import json
from threading import Thread
from jsonschema import validate, ValidationError
from json_io import JsonIO
from prepared_session_storage import PreparedSessionStorage
from balancing_report_generator import BalancingReportGenerator
from coverage_report_generator import CoverageReportGenerator
from learning_sets_generator import LearningSetsGenerator


class SegregationSystem:

    def __init__(self):
        self.segregation_system_config = None

    def import_config(self):
        config_path = os.path.join(os.path.abspath('..'), 'data', 'segregation_system_config.json')
        schema_path = os.path.join(os.path.abspath('..'), 'schemas',
                                   'segregation_system_config_schema.json')

        try:
            with open(config_path, encoding="UTF-8") as file:
                segregation_system_config = json.load(file)

            with open(schema_path, encoding="UTF-8") as file:
                segregation_system_config_schema = json.load(file)

            validate(segregation_system_config, segregation_system_config_schema)

        except FileNotFoundError:
            print('Failed to open segregation_system_config.json')
            print('Shutdown')
            sys.exit(1)

        except ValidationError:
            print('Config validation failed')
            print('Shutdown')
            sys.exit(1)

        self.segregation_system_config = segregation_system_config

    def save_config(self):
        config_path = os.path.join(os.path.abspath('..'), 'data', 'segregation_system_config.json')
        try:
            with open(config_path, "w", encoding="UTF-8") as file:
                json.dump(self.segregation_system_config, file, indent=4)
        except Exception as e:
            print(e)
            print('Failure to save segregation_system_config.json')
            return False
        return True

    def run(self):

        # start the listening server that will receive json messages
        listener = Thread(target=JsonIO.get_instance().listener, args=("0.0.0.0", "5000"))
        listener.setDaemon(True)
        listener.start()

        # import the configuration and initialize the PreparedSessionCollector
        self.import_config()
        collector = PreparedSessionStorage(self.segregation_system_config)
        collector.segregation_system_config = self.segregation_system_config

        # set the testing mode
        testing_mode = self.segregation_system_config['testing_mode']
        print(f"Testing mode: {testing_mode}")

        while True:
            stage = self.segregation_system_config['stage']

            print(f"Stage: {stage}")

            # --------------- STORE STAGE -------------------

            if stage == 'store':

                received_json = JsonIO.get_instance().receive()

                print(f"Received Json: {received_json}")

                if collector.store_prepared_session(received_json):
                    collector.increment_session_counter()
                else:
                    continue

                if not collector.check_max_sessions():
                    continue

                self.segregation_system_config['stage'] = 'balancing'
                self.save_config()
                continue

            # ---------------- BALANCING STAGE -----------------------

            elif stage == 'balancing':

                dataset = collector.load_dataset()
                if dataset is None:
                    print("Unable to load the database")
                    continue

                # Generate balancing chart and report
                balancing = BalancingReportGenerator()
                balancing_info = balancing.generate_chart(dataset)
                balancing.generate_report(balancing_info)

                # Evaluate balancing report
                response = balancing.evaluate_report()

                if response == 0:
                    # Dataset balanced, move to coverage stage
                    self.segregation_system_config['stage'] = 'coverage'
                    self.save_config()
                    continue

                elif response == -1:
                    # Dataset not balanced, a new configuration is sent with the missing samples
                    # Human interaction needed in this part
                    continue
                else:
                    # Handle return -2
                    print("Some error occured, shutting down")
                    sys.exit(0)

            # ---------------- COVERAGE STAGE -----------------------
            elif stage == 'coverage':

                dataset = collector.load_dataset()
                if dataset is None:
                    print("Unable to load the database")
                    continue

                # Generate coverage chart and report
                coverage = CoverageReportGenerator()
                coverage_info = coverage.generate_chart(dataset)

                # Evaluate coverage report
                coverage.generate_report(coverage_info)
                response = coverage.evaluate_report()

                if response == 0:
                    # The coverage is ok, move to learning stage
                    self.segregation_system_config['stage'] = 'learning'
                    self.save_config()
                    continue
                elif response == -1:
                    # The coverage is not ok, clean the db and restart
                    # the prepared sessions collection
                    collector.empty_db()
                    self.segregation_system_config['stage'] = 'store'
                    self.save_config()
                    continue
                else:
                    # Handle return -2
                    print("Some error occured, shutting down")
                    sys.exit(0)

            # ---------------- LEARNING SETS STAGE -----------------------
            elif stage == 'learning':

                learning = LearningSetsGenerator(self.segregation_system_config)
                dataset = collector.load_dataset()
                learning_sets = learning.generate_learning_sets(dataset)

                ip = self.segregation_system_config['development_system_ip']
                port = self.segregation_system_config['development_system_port']

                if JsonIO.get_instance().send(ip, port, learning_sets):
                    print("Learning sets successfully sent")

                    # The db is emptied in order to handle a new dataset
                    collector.empty_db()
                else:
                    print("Failed to send learning sets")

                # the dataset is evaluated and sent, so it's possible continue collecting new data
                # and build a new dataset
                self.segregation_system_config['stage'] = 'store'
                self.save_config()

                continue

            else:
                print('Invalid stage')
                print('Shutdown')
                sys.exit(1)

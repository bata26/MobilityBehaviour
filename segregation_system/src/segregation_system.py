import os
import sys
import time
import json
from threading import Thread
from jsonschema import validate, ValidationError
from src.json_io import JsonIO
from src.prepared_session_storage import PreparedSessionStorage
from src.balancing_report_generator import BalancingReportGenerator
from src.coverage_report_generator import CoverageReportGenerator
from src.learning_sets_generator import LearningSetsGenerator


class SegregationSystem:

    def __init__(self):
        self.segregation_system_config = None

    def import_config(self):
        config_path = os.path.join(os.path.abspath('.'), 'data', 'segregation_system_config.json')
        schema_path = os.path.join(os.path.abspath('.'), 'schemas',
                                   'segregation_system_config_schema.json')

        try:
            with open(config_path) as file:
                segregation_system_config = json.load(file)

            with open(schema_path) as file:
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
        config_path = os.path.join(os.path.abspath('.'), 'data', 'segregation_system_config.json')
        try:
            with open(config_path, "w") as file:
                json.dump(self.segregation_system_config, file, indent=4)
        except Exception as e:
            print(e)
            print('Failure to save segregation_system_config.json')
            return False
        return True

    def run(self):

        # import the configuration and initialize the prepared_session_collector
        self.import_config()
        collector = PreparedSessionStorage(self.segregation_system_config)
        collector.segregation_system_config = self.segregation_system_config

        # Start the listening server that will receive json messages
        # On MacOS port 5000 is used by AirPlay Receiver
        segregation_system_ip = self.segregation_system_config['segregation_system_ip']
        segregation_system_port = self.segregation_system_config['segregation_system_port']
        listener = Thread(target=JsonIO.get_instance().listener,
                          args=(segregation_system_ip, segregation_system_port))
        listener.setDaemon(True)
        listener.start()

        while JsonIO.get_instance().get_queue().get(block=True) is False:
            time.sleep(3)
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

                # The system need a new reconfiguration
                elif response == -1:
                    self.segregation_system_config['stage'] = 'store'
                    self.save_config()
                    print("Reconfiguration needed")
                    print("Shutdown")
                    sys.exit(0)
                    '''
                    sh = int(input("Enter how many shopping items are missing: "))
                    sp = int(input("Enter how many sport items are missing: "))
                    co = int(input("Enter how many cooking items are missing: "))
                    ga = int(input("Enter how many gaming items are missing: "))
                    request = dict(shopping=sh, sport=sp, cooking=co, gaming=ga)
                    ip = self.segregation_system_config['preparation_system_ip']
                    port = self.segregation_system_config['preparation_system_port']

                    # ENDPOINT MANCANTE
                    endpoint = 'prepared_session_endpoint'

                    # Send the request for missing samples
                    if JsonIO.get_instance().send(ip, port, endpoint, request):
                        print("Request successfully sent")

                        # Back to store phase to receive missing samples
                        self.segregation_system_config['stage'] = 'store'
                        self.save_config()

                    else:
                        print("Failed to send the request")
                        # If the request fails the balancing stage the system is
                        # set back to the store stage and the system is turned off
                        # for maintenance
                        self.segregation_system_config['stage'] = 'store'
                        self.save_config()
                        print("Shutdown")
                        sys.exit(0)
                    '''
                else:
                    # Handle return -2
                    print("Shutdown")
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

                # The system need a new reconfiguration
                elif response == -1:
                    self.segregation_system_config['stage'] = 'store'
                    self.save_config()
                    print("Reconfiguration needed")
                    print("Shutdown")
                    sys.exit(0)
                    '''
                    # When the endpoint is triggered i need a new dataset
                    # no request needed
                    request = None
                    ip = self.segregation_system_config['preparation_system_ip']
                    port = self.segregation_system_config['preparation_system_port']

                    # ENDPOINT MANCANTE
                    endpoint = 'prepared_session_endpoint'

                    # Send the request a new dataset
                    if JsonIO.get_instance().send(ip, port, endpoint, request):
                        print("Request successfully sent")

                        # Back to store phase to receive a new dataset
                        self.segregation_system_config['stage'] = 'store'
                        self.save_config()
                        
                        # The db is emptied in order to handle a new dataset
                        #collector.empty_db()

                    else:
                        print("Failed to send the request")
                        # If the request fails the coverage stage the system is
                        # set back to the store stage and the system is turned off
                        # for maintenance
                        self.segregation_system_config['stage'] = 'store'
                        self.save_config()
                        print("Shutdown")
                        sys.exit(0)
                    '''
                else:
                    # Handle return -2
                    print("Shutdown")
                    sys.exit(0)

            # ---------------- LEARNING SETS STAGE -----------------------
            elif stage == 'learning':

                learning = LearningSetsGenerator(self.segregation_system_config)
                dataset = collector.load_dataset()
                learning_sets = learning.generate_learning_sets(dataset)

                development_system_ip = self.segregation_system_config['development_system_ip']
                development_system_port = self.segregation_system_config['development_system_port']
                endpoint = 'senddata'

                if JsonIO.get_instance().send(
                    development_system_ip, development_system_port, endpoint, learning_sets):
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

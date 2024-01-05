import json
import os
import random
from time import time, sleep
from pandas import read_csv, DataFrame
from requests import post, exceptions
import logging

INGESTION_SYSTEM_IP = '127.0.0.1'
INGESTION_SYSTEM_PORT = 4000
#MISSING_SAMPLES = [9, 10, 11]

TESTING_MODE = True  # Enables timestamp saving
DATASET_TO_SEND = 100  # Dataset to test during the testing mode

CONFIG_FILENAME = 'ingestion_system_config.json'


def save_timestamp():
    t = time()
    df = DataFrame([[t]], columns=['Timestamp'])
    df.to_csv(f'timestamp-{t}.csv', index=False)


def is_queue_full() -> bool:
    try:
        with open(os.path.join(os.path.abspath('..'), 'data', 'queue_size.txt'), 'r') as f:
            queue_size = int(f.read())
            return queue_size > 2000
    except FileNotFoundError:
        return False
    except ValueError:
        return False


class ClientSimulation:
    def __init__(self):
        with open(os.path.join(os.path.abspath('..'), 'data', CONFIG_FILENAME)) as f:
            loaded_json = json.load(f)
            self.operative_mode = loaded_json['operative_mode']

            if self.operative_mode == 'production':
                self.production_window = loaded_json['production_window']
                self.evaluation_window = loaded_json['evaluation_window']
                self.missing_samples_threshold = loaded_json['missing_samples_threshold']
                self.sessions_executed = 0
                self.sessions_evaluated = 0
                self.evaluation = False

        self.dataset_length = None
        self.dataset = None
        self.missing_samples = []
        
    def send_record(self, data: dict) -> None:
        try:
            post(url=connection_string, json=data)
        except exceptions.RequestException:
            logging.error('Ingestion System unreachable')
            exit(-1)

    def read_dataset(self) -> None:
        
        time_series_df = read_csv('../csv/smartShoeSensors.csv')
        list = time_series_df.values.tolist()
        set_time_series = []
        
        for item in list:
            #print(item)
            missing_samples_counter = 0
            for i in range(1, len(item)):
                if random.random() < 0.1:
                    #logging.warning(item[i], f'Generating a missing sample')
                    #print(item[i])
                    item[i] = None
                    missing_samples_counter +=1
                    #print(missing_samples_counter)
            json = {
                "uuid":item[0],
                "time_series":item[1:]
            }
            set_time_series.append(json)
            self.missing_samples.append(missing_samples_counter)    
                 
        #headset = read_csv(os.path.join(os.path.abspath('..'), 'csv', 'brainControlledWheelchair_headset.csv'))
        #set_headset = headset.rename(columns={'CHANNEL': 'channel', 'TIMESTAMP': 'timestamp', 'UUID': 'uuid'})
        set_calendar = read_csv(os.path.join(os.path.abspath('..'), 'csv', 'calendar.csv'))
        set_environment = read_csv(os.path.join(os.path.abspath('..'), 'csv', 'environment.csv'))
        labels = read_csv(os.path.join(os.path.abspath('..'), 'csv', 'labels.csv'))
        set_labels = labels[['label', 'uuid']].rename(columns={'label': 'pressure_detected', 'uuid': 'uuid'})

        self.dataset = [
            {
                'name': 'calendar',
                'records': set_calendar
            }, {
                'name': 'label',
                'records': set_labels
            }, {
                'name': 'environment',
                'records': set_environment
            }, {
                'name': 'time_series',
                'records': set_time_series,
            }]
        self.dataset_length = len(self.dataset[0]['records'])

    def send_dataset(self, dataset_counter: int) -> None:
        if self.operative_mode == 'development':
            self.development_mode(dataset_counter=dataset_counter)
        else:
            self.production_mode(dataset_counter=dataset_counter)

    def development_mode(self, dataset_counter: int) -> None:
        catch_timestamp = True

        for session_index in range(0, self.dataset_length):
            # Shuffle in order to create non-synchronized records
            random.shuffle(self.dataset)

            # while is_queue_full():
            #     trace('Ingestion queue full..waiting for 50 sec')
            #     sleep(50)

            logging.info('', '============================ START SESSION ============================', 0)
            for i in range(0, len(self.dataset)):
                if self.dataset[i]['name'] == 'time_series':
                    # Read the data in the dataset
                    record = self.dataset[i]['records'][session_index]
                    print(record)
                    logging.info(record["uuid"], f'Sending time series [tim {record["time_series"]}', 1)
                    self.send_record(data=record)

                    # In order to get a timestamp in case of testing mode
                    if TESTING_MODE and dataset_counter == 0 and catch_timestamp:
                        save_timestamp()
                        catch_timestamp = False
                else:
                    record = self.dataset[i]['records'].loc[session_index].to_dict()
                    print(record)
                    if random.random() < 0.1 and self.dataset[i]["name"] != 'label':
                        logging.warning(record["uuid"], f'Generating a missing sample [{self.dataset[i]["name"]}]')
                    else:
                        logging.warning(record["uuid"], f'Sending {self.dataset[i]["name"]} data', 1)
                        self.send_record(data=record)

                        # In order to get a timestamp in case of testing mode
                        if TESTING_MODE and dataset_counter == 0 and catch_timestamp:
                            save_timestamp()
                            catch_timestamp = False

            # Send a session very X milliseconds
            sleep(2)

    def production_mode(self, dataset_counter: int) -> None:
        catch_timestamp = True

        for session_index in range(0, self.dataset_length):
            # Counter related to a single session
            missing_records = 0
            
            # Shuffle in order to create non-synchronized records
            random.shuffle(self.dataset)

            # while is_queue_full():
            #     trace('Ingestion queue full..waiting for 50 sec')
            #     sleep(50)

            logging.info('', '============================ START SESSION ============================', 0)
            for i in range(0, len(self.dataset)):
                if self.dataset[i]['name'] == 'time_series':
                    
                    # Read the data in the dataset
                    record = self.dataset[i]['records'][session_index]
                    print(record)                        
                    logging.info(record['uuid'], f'Sending time_series', 1)
                    self.send_record(data=record)

                    # In order to get a timestamp in case of testing mode
                    if TESTING_MODE and dataset_counter == 0 and catch_timestamp:
                        save_timestamp()
                        catch_timestamp = False
                else:
                    if self.dataset[i]["name"] == 'label':
                        if self.evaluation:
                            record = self.dataset[i]['records'].loc[session_index].to_dict()
                            logging.info(record["uuid"], f'Sending {self.dataset[i]["name"]} data', 1)
                            self.send_record(data=record)

                            # In order to get a timestamp in case of testing mode
                            if TESTING_MODE and dataset_counter == 0 and catch_timestamp:
                                save_timestamp()
                                catch_timestamp = False
                        else:
                            # Drop the label (it is not needed)
                            pass
                    elif self.dataset[i]["name"] == 'time_series':
                        record = self.dataset[i]['records'][session_index]
                        self.send_record(data=record)
                    else:    
                        if random.random() < 0.1 and not self.evaluation:
                            logging.warning(record["uuid"],f'Generating a missing sample [{self.dataset[i]["name"]}]')
                            missing_records += 1
                        else:
                            record = self.dataset[i]['records'].loc[session_index].to_dict()
                            #if the session will be discarded because the threshold is not satisfied
                            # the label will be lost
                            logging.info(record["uuid"], f'Sending {self.dataset[i]["name"]} data', 1)
                            self.send_record(data=record)
                        
                        # In order to get a timestamp in case of testing mode
                        if TESTING_MODE and dataset_counter == 0 and catch_timestamp:
                            save_timestamp()
                            catch_timestamp = False

            # Update operative mode phase (production or evaluation)
            self.check_current_phase(missing_samples=self.missing_samples[session_index], missing_records=missing_records)

            # Send a session very X milliseconds
            sleep(2)

    def check_current_phase(self, missing_samples: int, missing_records: int):
        if not self.evaluation:
            if not (missing_records > 0 or missing_samples > self.missing_samples_threshold):
                self.sessions_executed += 1
                logging.info(f'Complete session sent to the Ingestion System: {self.sessions_executed}')

                if self.sessions_executed == self.production_window:
                    logging.info(f'Starting evaluation Phase...')
                    self.sessions_executed = 0
                    self.evaluation = True
        else:
            self.sessions_evaluated += 1
            if self.sessions_evaluated == self.evaluation_window:
                logging.info(f'Evaluation phase ended. Sessions evaluated: {self.sessions_evaluated}')
                self.sessions_evaluated = 0
                self.evaluation = False


if __name__ == '__main__':
    connection_string = f'http://{INGESTION_SYSTEM_IP}:{INGESTION_SYSTEM_PORT}/record'
    logging.info('', f'Connection to {connection_string}', 2)
    logging.info('', f'Testing mode: {TESTING_MODE}\n', 2)

    data_sources_sim = ClientSimulation()
    data_sources_sim.read_dataset()

    for j in range(0, DATASET_TO_SEND):
        logging.info('', f'Sending Dataset #{j + 1}', 0)
        data_sources_sim.send_dataset(dataset_counter=j)

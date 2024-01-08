import os
import sys
import sqlite3
import json
import logging
from jsonschema import validate, ValidationError
from src.ingestion_system_configuration import IngestionSystemConfiguration

RECORD_TYPE = ['calendar', 'pressure_detected', 'environment', 'time_series']
NUM_COLUMNS = 1236
CONFIG_PATH = './data/ingestion_system_config.json'
CONFIG_SCHEMA_PATH = './data/ingestion_system_config_schema.json'

class RawSessionsStore:
    """
    This class is responsible for handling the database operations.
    """
    def __init__(self) -> None:
        """
        Initializes the Raw Sessions Store
        """
        self.conn = None
        self.configuration = IngestionSystemConfiguration(CONFIG_PATH, CONFIG_SCHEMA_PATH)

        db_path = os.path.join(os.path.abspath('..'), self.configuration.db_name)
        if os.path.exists(db_path):
            # print('[+] sqlite3 previous database deleted')
            os.remove(db_path)

        if self.open_connection() and self.create_table():
            # print('[+] sqlite3 connection established and raw_session table initialized')
            pass
        else:
            logging.error('sqlite3 initialize failed')
            sys.exit(1)

    def open_connection(self) -> bool:
        """
        Creates the connection to the database
        :return: True if the connection is successful. False if the connection fails.
        """
        try:
            self.conn = sqlite3.connect(os.path.join(os.path.abspath('..'), self.configuration.db_name))
            return True
        except sqlite3.Error as e:
            logging.error('sqlite3 open connection error %s', e)

        return False

    def close_connection(self) -> None:
        """
        Closes the connection to the database
        :return: True if the disconnection is successful. False otherwise.
        """
        try:
            self.conn.close()
        except sqlite3.Error as e:
            logging.error('sqlite3 close connection error %s', e)
            sys.exit(1)

    def check_connection(self) -> None:
        """
        Checks if the connection with the database is established.
        It terminates the system if the connection is not set.
        """
        if self.conn is None:
            logging.error('sqlite3 connection not established')
            sys.exit(1)

    def create_table(self) -> bool:
        """
        Creates the table used to synchronize records and join them in order to build a Raw Session
        :return: True if the creation is successful. False otherwise.
        """
        self.check_connection()

        try:
            series_columns = str()
            for i in range(1, NUM_COLUMNS + 1):
                series_columns += RECORD_TYPE[3] + '_' + str(i) + ' TEXT, '

            query = 'CREATE TABLE IF NOT EXISTS raw_session ( \
                uuid TEXT NOT NULL, \
                ' + RECORD_TYPE[0] + ' TEXT, \
                ' + RECORD_TYPE[1] + ' TEXT, \
                ' + RECORD_TYPE[2] + ' TEXT, \
                ' + series_columns + \
                    'UNIQUE(uuid), PRIMARY KEY (uuid))'
            self.conn.cursor().execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error('sqlite3 "create_tables" error %s', e)
            return False

        return True

    def get_record_type(self, record: dict) -> str:
        """
        Identifies the record type. The possible ones are calendar, pressure_detected, 
        environment and time_series.
        :param record: record to identify
        :return: type of the record
        """
        keys = list(record.keys())[0:2]

        for record_type in RECORD_TYPE:
            if record_type in keys:
                return record_type
        return 'None'

    def validate_schema_record(self, record: dict, record_type: str) -> bool:
        """
        Validates a received record given a pre-defined schema
        :param record: dictionary that represents the received record
        :param record_type: type of the record to validate
        :return: True if the validation is successful. False if the validation fails.
        """
        try:
            record_schema_path = os.path.join('data', record_type + '_schema.json')
            with open(record_schema_path) as f:
                loaded_schema = json.load(f)
                validate(record, loaded_schema)

        except ValidationError:
            logging.error('Record schema validation failed')
            return False

        except FileNotFoundError:
            logging.error('Failed to open schema path %s', record_type)
            exit(-1)

        return True

    def raw_session_exists(self, uuid: str) -> bool:
        """
        Checks if already exists a Raw Session in the Data Store
        :param uuid: string representing the Raw Session to check
        :return: True if the Raw Session exists. False otherwise
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT COUNT(1) FROM raw_session WHERE uuid = ?', (uuid, ))
            self.conn.commit()

            result = cursor.fetchone()
            if result[0] == 0:
                return False

        except sqlite3.Error as e:
            logging.error('sqlite3 "raw_session_exists" error %s', e)
            return False

        return True

    def store_record(self, record: dict) -> bool:
        """
        Stores the received record into the database after its type identification and validation.
        :param record: dictionary representing the received record to store
        :return: True if the store is successful. False if it fails.
        """
        self.check_connection()

        # Get record type in order to save it in the correct column the record
        record_type = self.get_record_type(record)

        # Record validation
        if not self.validate_schema_record(record, record_type):
            logging.error('Record schema not valid (record discarded)')
            return False

        # Check if the record received belongs to a session whose synchronization is taking place
        if self.raw_session_exists(record['uuid']):
            # Update the Raw Session row
            column_name = record_type
            query_result = self.update_raw_session(record=record, column_to_set=column_name)
        else:
            # Insert a new Raw Session row with only one column containing the record received
            query_parameters = self.generate_insert_parameters(record=record, \
                                                               record_type=record_type)
            query_result = self.insert_raw_session(parameters=query_parameters)

        return query_result

    def generate_insert_parameters(self, record: dict, record_type: str) -> tuple:
        """
        Generates parameters for the insertion of a new Raw Session
        """
        parameters = {
            'uuid': record['uuid'],
            'calendar': None,
            'pressure_detected': None,
            'environment': None,
            'time_series': [None] * NUM_COLUMNS
        }

        parameters[record_type] = record[record_type]
        values = list(parameters.values())
        query_parameters = values[0:-1] + values[-1]
        return tuple(query_parameters)

    def insert_raw_session(self, parameters: tuple) -> bool:
        """
        Inserts a Raw Session in the database upon receiving a record belonging to a new session
        :param parameters: query parameters in order to set the right column
        :return: True if the insert is successful. False otherwise.
        """
        try:
            series_columns = str()
            for i in range(1, NUM_COLUMNS + 1):
                series_columns += RECORD_TYPE[3] + '_' + str(i)
                if i == NUM_COLUMNS:
                    series_columns += ")"
                else:
                    series_columns += ','
            series_columns += 'VALUES (?,?,?,?,'
            for i in range(1, NUM_COLUMNS + 1):
                series_columns += '?'
                if i == NUM_COLUMNS:
                    series_columns += ")"
                else:
                    series_columns += ','

            query = 'INSERT INTO raw_session (uuid, calendar, pressure_detected, environment, ' \
                    + series_columns

            cursor = self.conn.cursor()
            cursor.execute(query, parameters)
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error('sqlite3 "insert_raw_session" error %s', e)
            return False

        return True

    def update_raw_session(self, record: dict, column_to_set: str) -> bool:
        """
        Updates a Raw Session in the database upon receiving a record 
        belonging to a session already in the database
        :param record: dictionary representing the received record to store
        :param column_to_set: column to update
        :return: True if the update is successful. False otherwise.
        """
        try:
            if column_to_set == 'time_series':
                for i in range(1, NUM_COLUMNS + 1):
                    column_name = column_to_set + '_' + str(i)
                    query = 'UPDATE raw_session SET ' + column_name + ' = ? WHERE uuid = ?'
                    cursor = self.conn.cursor()
                    cursor.execute(query, (record[column_to_set][i-1], record['uuid']))
                    self.conn.commit()
            else:
                query = 'UPDATE raw_session SET ' + column_to_set + ' = ? WHERE uuid = ?'
                cursor = self.conn.cursor()
                cursor.execute(query, (record[column_to_set], record['uuid']))
                self.conn.commit()
        except sqlite3.Error as e:
            logging.error('sqlite3 "update_raw_session" error %s', e)
            return False

        return True

    def delete_raw_session(self, uuid: str) -> bool:
        """
        Deletes a Raw Session from the data store
        :param uuid: string that represents the primary key of the row to delete form the data store
        :return: True if the 'delete' is successful. False otherwise.
        """
        self.check_connection()

        try:
            query = 'DELETE FROM raw_session WHERE uuid = ?'
            cursor = self.conn.cursor()
            cursor.execute(query, (uuid, ))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error('sqlite3 "delete_raw_session" error %s', e)
            return False

        return True

    def load_raw_session(self, uuid: str) -> dict:
        """
        Loads a Raw Session from the data store
        :param uuid: string that represents the primary key of the row to load from the data store
        :return: dictionary representing the loaded Raw Session
        """
        self.check_connection()

        try:
            query = 'SELECT * FROM raw_session WHERE uuid = ?'
            cursor = self.conn.cursor()
            cursor.execute(query, (uuid, ))
            self.conn.commit()

            result = cursor.fetchone()
            if result is None:
                return {}

            # Building the loaded Raw Session as a dictionary
            raw_session = {
                'uuid': result[0],
                'calendar': result[1],
                'pressure_detected': 'None',
                'environment': result[3],
                'time_series': []
            }

            # Handling missing label
            if result[2] is not None:
                raw_session['pressure_detected'] = result[2]
            for ts in result[4:]:
                if ts is not None:
                    ts_json = json.loads(ts)
                    #ts_data = list(ts_json.values())
                    raw_session['time_series'].append(ts_json)
            return raw_session
        except sqlite3.Error as e:
            logging.error('sqlite3 "load_raw_session" error %s', e)
            return {}

    def is_session_complete(self, uuid: str, last_missing_sample: bool, evaluation: bool) -> bool:
        """
        Checks if the synchronization and building of the Raw Session 
        has been completed meaning there are no more records related to the session.
        :param last_missing_sample:
        :param uuid: string that identifies the session to check
        :param evaluation: boolean that says if the label has to be a required field or not
        :return: True if the session is completed. False otherwise.
        """
        self.check_connection()
        operative_mode = self.configuration.operative_mode
        try:
            if last_missing_sample:
                # Since last_missing_samples is True it means that
                # there will be no more records related to this session
                # So the task to check if the session is good or not is
                # shifted to the RawSessionIntegrity class
                # Here the only important thing is to check if the required fields are not missing
                query = 'SELECT COUNT(1) FROM raw_session WHERE uuid = ? ' \
                        + 'AND calendar IS NOT NULL AND environment IS NOT NULL ' \
                        + ('AND pressure_detected IS NOT NULL' if (operative_mode == 'development' \
                                                                    or evaluation) else '')
            else:
                # The session is still in the synchronization/building phase,
                # So it is necessary to check all the possible fields
                # (except for the labels during the production mode)
                # If all the records are not null, the session can be labeled as 'fully complete'
                series_columns = str()
                for i in range(1, 100):
                    series_columns += ' AND ' + RECORD_TYPE[3] + '_' + str(i) + ' IS NOT NULL '

                query = 'SELECT COUNT(1) FROM raw_session WHERE uuid = ? ' \
                        + 'AND calendar IS NOT NULL AND environment IS NOT NULL ' \
                        + ('AND pressure_detected IS NOT NULL' if (operative_mode == 'development' \
                                                                     or evaluation) else ' ') \
                        + series_columns

            cursor = self.conn.cursor()
            cursor.execute(query, (uuid, ))
            self.conn.commit()

            result = cursor.fetchone()
            if result[0] == 0:
                return False

        except sqlite3.Error as e:
            logging.error('sqlite3 "is_session_complete" error %s', e)
            return False

        return True

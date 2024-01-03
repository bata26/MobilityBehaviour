import os
import sys
import json
import sqlite3
from jsonschema import validate, ValidationError

class PreparedSessionStorage:

    def __init__(self, config):
        self.segregation_system_config = config
        self.prepared_session_counter = 0

        db_name = config['db_name']
        db_path = os.path.join(os.path.abspath('.'), 'data', db_name)
        if not os.path.exists(db_path):
            print("Sqlite db doesn't exist")
            sys.exit(1)
        try:
            self._conn = sqlite3.connect(db_path)
        except sqlite3.Error as e:
            print(f'[-] Sqlite Connection Error [{e}]')
            sys.exit(1)

    def increment_session_counter(self):
        self.prepared_session_counter = self.prepared_session_counter + 1

    def check_max_sessions(self):

        # If the sessions number is big enough a learning session set is completed
        max_sessions = self.segregation_system_config['max_sessions']
        if self.prepared_session_counter >= max_sessions:
            self.prepared_session_counter = 0
            return True
        else:
            return False

    def validate_prepared_session(self, prepared_session):
        schema_path = os.path.join(os.path.abspath('.'), 'schemas', 'prepared_session_schema.json')
        try:

            with open(schema_path) as file:
                prepared_session_schema = json.load(file)

            validate(prepared_session, prepared_session_schema)

        except FileNotFoundError:
            print('Failure to open prepared_session_schema.json')
            return False

        except ValidationError:
            print('Prepared Session validation failed')
            return False

        return True

    def load_dataset(self):

        # devo fetchare tutto il db
        query = "SELECT * FROM info JOIN features USING (_id)"
        cursor = self._conn.cursor()
        try:
            cursor.execute(query)
        except sqlite3.Error as e:
            print(f'Sqlite Execution Error [{e}]')
            return None

        response = cursor.fetchall()
        if response is None:
            return None

        # save the dataset as a list of prepared sessions
        dataset = []

        for prepared_session in response:
            prepared_list = list(prepared_session)
            session = {}
            session['_id'] = prepared_list[0]
            session['calendar'] = prepared_list[1]
            session['environment'] = prepared_list[2]
            session['label'] = prepared_list[9]
            session['features'] = {
                'maximum_pressure_ts' : prepared_list[3],
                'minimum_pressure_ts' : prepared_list[4],
                'median_pressure_ts' : prepared_list[5],
                'mean_absolute_deviation_pressure_ts' : prepared_list[6],
                'activity_and_small_scatter' : prepared_list[7],
                'environment_and_small_scatter' : prepared_list[8]
            }
            dataset.append(session)
        return dataset

    def store_prepared_session(self, prepared_session):

        # Validate before storing session
        if not self.validate_prepared_session(prepared_session):
            print("Invalid data")
            return False

        # Store the prepared session data between info e features table
        info = "INSERT INTO info (_id, calendar, environment) \
            VALUES(?, ?, ?)"

        features = "INSERT INTO features (_id, maximum_pressure_ts, minimum_pressure_ts, \
            median_pressure_ts, mean_absolute_deviation_pressure_ts, activity_and_small_scatter, \
                environment_and_small_scatter, label) \
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?)"

        cursor = self._conn.cursor()

        try:
            cursor.execute(info, (prepared_session['_id'],
                                   prepared_session['calendar'],
                                   prepared_session['environment']))

            cursor.execute(features, (prepared_session['_id'],
                           prepared_session['features']['maximum_pressure_ts'],
                           prepared_session['features']['minimum_pressure_ts'],
                           prepared_session['features']['median_pressure_ts'],
                           prepared_session['features']['mean_absolute_deviation_pressure_ts'],
                           prepared_session['features']['activity_and_small_scatter'],
                           prepared_session['features']['environment_and_small_scatter'],
                           prepared_session['label']))

            self._conn.commit()
        except sqlite3.Error as e:
            print(f"[-] Sqlite Execution Error [{e}]")
            return False

        print(f"Stored new prepared session (_id: {prepared_session['_id']} calendar: {prepared_session['calendar']})")
        return True

    def empty_db(self):

        info = "DELETE FROM info"
        features = "DELETE FROM features"
        cursor = self._conn.cursor()

        try:
            cursor.execute(info)
            cursor.execute(features)
            self._conn.commit()
        except sqlite3.Error as e:
            print(f"[-] Sqlite Execution Error [{e}]")
            return False

        print("The database has been emptied")
        return True

import os
import sys
import json
import sqlite3
from jsonschema import validate, ValidationError

class LabelStorage:

    def __init__(self, config):
        self.evaluation_system_config = config

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

    def validate_label(self, label):
        schema_path = os.path.join(os.path.abspath('.'), 'schemas', 'label_schema.json')
        try:

            with open(schema_path) as file:
                label_schema = json.load(file)

            validate(label, label_schema)

        except FileNotFoundError:
            print('Failure to open prepared_session_schema.json')
            return False

        except ValidationError:
            print('Prepared Session validation failed')
            return False

        return True

    def load_labels(self):
        query = "SELECT * FROM label"
        cursor = self._conn.cursor()
        try:
            cursor.execute(query)
        except sqlite3.Error as e:
            print(f'Sqlite Execution Error [{e}]')
            return None

        response = cursor.fetchall()
        if response is None:
            return None

        labels = []

        for label in response:
            lab = {}
            lab['_id'] = label[0]
            lab['label'] = label[1]
            labels.append(label)
        return labels


    def store_label(self, label):

        # Validate before storing label
        if not self.validate_label(label):
            print("Invalid data")
            return False

        query = "INSERT INTO label (_id, label) VALUES(?, ?)"

        cursor = self._conn.cursor()


        try:
            cursor.execute(query, label['_id'], label['label'])
            self._conn.commit()
        except sqlite3.Error as e:
            print(f"[-] Sqlite Execution Error [{e}]")
            return False

        print(f"Stored new label (_id: {label['_id']} calendar: {label['label']})")
        return True
    
    def empty_db(self):
        query = "DELETE FROM label"
        cursor = self._conn.cursor()

        try:
            cursor.execute(query)
            self._conn.commit()
        except sqlite3.Error as e:
            print(f"[-] Sqlite Execution Error [{e}]")
            return False

        print("The database has been emptied")
        return True
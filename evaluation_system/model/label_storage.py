import os
import sys
import json
import sqlite3
import threading
from jsonschema import validate, ValidationError
import pandas as pd

from model.labels import Label
from model.evaluation_report_generator import EvaluationReportGenerator


def validate_label(label):
    schema_path = os.path.join(os.path.abspath('.'), 'data\\schemas', 'label_schema.json')
    try:

        with open(schema_path) as file:
            label_schema = json.load(file)

        validate(label, label_schema)

    except FileNotFoundError:
        print('Failure to open label schema')
        return False

    except ValidationError:
        print('Label schema validation failed')
        return False

    return True


class LabelStorage:

    def __init__(self, config):
        self.config = config
        self.report = EvaluationReportGenerator(config)
        self.labels = None
        self.semaphore = threading.Semaphore(1)
        self.tot_labels_received = 0
        db_name = config.db_name
        db_path = os.path.join('.\data', db_name)

        if not os.path.exists(db_path):
            print("Database doesn't exist")
            sys.exit(1)
        try:
            self._conn = sqlite3.connect(db_path)
        except sqlite3.Error as e:
            print(f'[-] Sqlite Connection Error [{e}]')
            sys.exit(1)

    def read_sql(self, query: str):
        return pd.read_sql(query, self._conn)

    def run_query(self, query: str):
        cursor = self._conn.cursor()
        try:
            cursor.execute(query)
            self._conn.commit()
        except sqlite3.Error as e:
            print(f'Sqlite Execution Error [{e}]')
            return None

    def create_tables(self):
        print("Create tables (if not exists) for label storage")
        query = "CREATE TABLE if not exists expertLabel" \
                "(uuid TEXT PRIMARY KEY UNIQUE, label TEXT)"
        self.run_query(query)
        query = "CREATE TABLE if not exists classifierLabel" \
                "(uuid TEXT PRIMARY KEY UNIQUE, label TEXT)"
        self.run_query(query)

    def store_label(self, label):

        if not validate_label(label):
            print("Invalid label data format")
            return False

        with self.semaphore:
            uuid = label["uuid"]
            source = label["source"]
            label = label["label"]
            label = Label(uuid, label, source)
            label_dataframe = pd.DataFrame(label.to_dict(), index=[0], columns=["uuid", "label"])

            if label.source == 'classifier':
                try:
                    label_dataframe.to_sql('classifierLabel', self._conn, if_exists="append", index=False)
                    self.tot_labels_received += 1
                except Exception as e:
                    print("Error occured while inserting label")

            else:
                try:
                    label_dataframe.to_sql('expertLabel', self._conn, if_exists="append", index=False)
                    self.tot_labels_received += 1

                except Exception as e:
                    print("Error occured while inserting label")
                print(self.tot_labels_received)

            if self.tot_labels_received >= self.config.sufficient_labels:
                self.tot_labels_received -= self.config.sufficient_labels
                print("Generating Report")

                query = "SELECT expert.uuid, " \
                        "expert.label as expertLabel," \
                        "classifier.label as classifierLabel " \
                        "FROM expertLabel AS expert " \
                        "INNER JOIN classifierLabel AS classifier " \
                        "ON expert.uuid = classifier.uuid"

                labels = self.read_sql(query)

                uuid_list = labels["uuid"].to_list()

                if uuid_list:
                    self.empty_db(uuid_list)

                thread = threading.Thread(target=self.report.generate_report, args=[labels])
                thread.start()

    def empty_db(self, uuid_list):

        self.run_query(f"DELETE FROM expertLabel")
        self.run_query(f"DELETE FROM classifierLabel")
        print("Label tables cleaned")
        return True

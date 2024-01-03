import sqlite3
import time
from requests import post, exceptions

TABLES = ["calendar", "environment", "labels", "smartShoeSensors"]
DB_NAME = "input.db"
URI = "http://127.0.0.1:4000/record"
if __name__ == "__main__":
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # get list of id
    cursor.execute("SELECT distinct(uuid) FROM calendar")
    id_list = cursor.fetchall()
    # for each uuid execute a query from all tables
    for uuid in id_list:
        # extract the uuid from the tuple result
        selected_uuid = uuid[0]
        time.sleep(6)
        for table in TABLES:
            request_body = {"uuid": selected_uuid}
            cursor.execute(f"SELECT * from {table} WHERE uuid = '{selected_uuid}'")
            res = cursor.fetchone()
            print(table)
            if table == "calendar":
                request_body["calendar"] = res[1]
            elif table == "environment":
                request_body["environment"] = res[1]
            elif table == "labels":
                request_body["pressure_detected"] = res[1]
            else:
                request_body["time_series"] = []
                for index, value in enumerate(res):
                    if index == 0:
                        continue
                    request_body["time_series"].append(value)
            try:
                response = post(url=URI, json=request_body, timeout=3)
                if response.status_code != 200:
                    error_message = response.json()["error"]
                    print(f"Error: {error_message}")
                    exit(-1)
            except exceptions.RequestException:
                print(f"{URI} unreachable")
                exit(-1)

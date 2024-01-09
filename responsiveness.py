import time
import sqlite3
import requests
import pandas as pd

DB_NAME = "segregation.db"
INFO_TABLE_NAME = "info"
FEATURE_TABLE_NAME = "features"
URI = "http://127.0.0.1:6001/preparedsession"
"""
{
    _id [0]
    calendar [1]
    environment [2]
    label [10]
    features : 
        {
            maximum_pressure_ts [4]
            minimum_pressure_ts [5]
            median_pressure_ts [6]
            mean_absolute_deviation_pressure_ts [7]
            activity_and_small_scatter [8]
            environment_and_small_scatter [9]
        }
    
}
"""


def elaborate_data(query_result):
    elaborated = []
    for res in query_result:
        obj = {
            "_id": res[0],
            "calendar": res[1],
            "environment": res[2],
            "label": res[10],
            "features": {
                "maximum_pressure_ts": res[4],
                "minimum_pressure_ts": res[5],
                "median_pressure_ts": res[6],
                "mean_absolute_deviation_pressure_ts": res[7],
                "activity_and_small_scatter": res[8],
                "environment_and_small_scatter": res[9],
            },
        }
        elaborated.append(obj)
    return elaborated


def get_db_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
                   SELECT * 
                   FROM info
                   inner join features on info._id = features._id
                   """
    )
    res = cursor.fetchall()
    return res

def send_label(data):
    for index,item in enumerate(data):
        print(f"[INFO] {str(time.time())} Sending request # {index}")
        try:
            requests.post(URI , json=item)
        except Exception as e:
            print(f"[ERROR] Impossible to send request # {index}")

        #time.sleep(1)    

def elaborate_csv():
    files = ["res-0.csv" , "res-1s.csv"]

    for file in files:
        df = pd.read_csv(file)
        for ind in df.index:
            start = df["start"][ind]
            end = df["end"][ind]
            df["diff"][ind] = end - start
        
        df.to_csv(file)


if __name__ == "__main__":
    elaborate_csv()
    #query_result = get_db_data()
    #elaborated_data = elaborate_data(query_result)
    #send_label(elaborated_data)

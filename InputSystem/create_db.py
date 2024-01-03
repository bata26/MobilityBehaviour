import os
import pandas as pd
import sqlite3

DB_NAME = "input.db"
DIR_PATH = "./csv/"
def csv_to_sql():
    connection = sqlite3.connect(DB_NAME)

    for file in os.listdir(DIR_PATH):
        file_path = DIR_PATH + file
        print(file_path)
        df = pd.read_csv(file_path)
        table_name = file.split(".csv")[0]
        df.to_sql(table_name , connection, if_exists="append" , index=False)

if __name__ == '__main__':
    csv_to_sql()

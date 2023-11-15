import pandas as pd
from db import Db
from dotenv import load_dotenv
import os

CALENDAR_PATH = "./mobilityShoes/calendar.csv"
ENVIRONMENT_PATH = "./mobilityShoes/environment.csv"
LABELS_PATH = "./mobilityShoes/labels.csv"
SENSOR_DATA_PATH = "./mobilityShoes/smartShoeSensors.csv"

def getDataFromFile(filename):
    df = pd.read_csv(filename)
    return df.to_dict('records')

def setupCalendarTable():
    creationString = f"""
                    CREATE TABLE IF NOT EXISTS {os.getenv('CALENDAR_TABLE')}(
                    _id VARCHAR(50) PRIMARY KEY,
                    activity VARCHAR(50) NOT NULL
                    )
                    """
    if Db.createTable(os.getenv("CALENDAR_TABLE"), creationString):
        return True
    else:
        print("CALENDAR TABLE CREATION ABORTED")
        return False


def setupEnvironmentTable():
    creationString = f"""
                    CREATE TABLE IF NOT EXISTS {os.getenv("ENVIRONMENT_TABLE")}(
                    _id VARCHAR(50) PRIMARY KEY,
                    environment VARCHAR(50) NOT NULL
                    )
                    """
    if Db.createTable(os.getenv("ENVIRONMENT_TABLE"), creationString):
        return True
    else:
        print("ENVIRONMENT TABLE CREATION ABORTED")
        return False

def setupLabelsTable():
    creationString = f"""
                    CREATE TABLE IF NOT EXISTS {os.getenv("LABEL_TABLE")}(
                    _id VARCHAR(50) PRIMARY KEY,
                    anomalous VARCHAR(50) NOT NULL
                    )
                    """
    if Db.createTable(os.getenv("LABEL_TABLE"), creationString):
        return True
    else:
        print("LABELS TABLE CREATION ABORTED")
        return False

def setupSensorDataTable():
    data = getDataFromFile(SENSOR_DATA_PATH)
    db = Db.getInstance()
    creationString = f"""
                    CREATE TABLE IF NOT EXISTS {os.getenv("SENSOR_DATA_TABLE")}(
                    _id VARCHAR(50) PRIMARY KEY """
    row = data[0]
    for key in row.keys():
        if key == "_id":
            continue
        creationString += f", {key} LONG NOT NULL "
    creationString += ")"

    if Db.createTable(os.getenv("SENSOR_DATA_TABLE"), creationString):
        return True
    else:
        print("SENSOR DATA TABLE CREATION ABORTED")
        return False


def CsvToSql():
    conn = Db.getInstance()
    
    calendar = pd.read_csv(CALENDAR_PATH)
    calendar.to_sql(os.getenv("CALENDAR_TABLE"), conn, if_exists='replace', index = False)

    labels = pd.read_csv(LABELS_PATH)
    labels.to_sql(os.getenv("LABEL_TABLE"), conn, if_exists='replace', index = False)

    environment = pd.read_csv(ENVIRONMENT_PATH)
    environment.to_sql(os.getenv("ENVIRONMENT_TABLE"), conn, if_exists='replace', index = False)

    sensor_data = pd.read_csv(SENSOR_DATA_PATH)
    sensor_data.to_sql(os.getenv("SENSOR_DATA_TABLE"), conn, if_exists='replace', index = False)


if __name__ == "__main__":
    print("STARTING CREATING DATABASE")
    print("STARTING CALENDAR TABLE")
    if not(setupCalendarTable()):
        print("ABORTED")
        exit()
    print("CALENDAR SETUP COMPLETED")

    print("STARTING LABEL TABLE")
    if not(setupLabelsTable()):
        print("ABORTED")
        exit()
    print("LABEL SETUP COMPLETED")

    print("STARTING ENVIRONMENT TABLE")
    if not(setupEnvironmentTable()):
        print("ABORTED")
        exit()
    print("ENVIRONMENT SETUP COMPLETED")

    print("STARTING SENSOR DATA TABLE")
    if not(setupSensorDataTable()):
        print("ABORTED")
        exit()
    print("SENSOR DATA SETUP COMPLETED")

    CsvToSql()
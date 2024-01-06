import os
import time
import random
import pandas as pd
from model.db import Db
from model.msg_manager import MessageManager

class Dataset:
    CSV_DIR = "./csv/"
    ACTIVITY = ["shopping" , "gaming" , "sport" , "cooking" ]
    @staticmethod
    def fill_db():
        connection = Db.get_instance().get_connection()
        try:
            for file in os.listdir(Dataset.CSV_DIR):
                file_path = Dataset.CSV_DIR + file
                print(file_path)
                df = pd.read_csv(file_path)
                table_name = file.split(".csv")[0]
                df.to_sql(table_name , connection, index=False)
        except Exception as e:
            print("[ERROR] Impossible to fill db" , str(e))
            raise e
    """
    STRUCT:
    [0:1] -> uuid,labels
    [2:3] -> uuid,env
    [4:5] -> uuid,activity
    [6:]  -> uuid, ts

    elaboratedData:
    "activity":[
        {
            "uuid",
            "env",
            "label",
            "ts" : []
        }
    ]
    """
    @staticmethod
    def elaborate_data(samples):
        res = {
            "shopping":[] , 
            "gaming": [] , 
            "sport":[] , 
            "cooking":[],
        }

        for sample in samples:

            uuid = sample[0]
            label = sample[1]
            environment = sample[3]
            activity = sample[5]
            ts = [value for value in sample[7:]]

            obj = {
                "uuid": uuid,
                "environment": environment,
                "label": label,
                "activity": activity,
                "ts" : ts,
            }

            res[activity].append(obj)
        return res
    @staticmethod
    def send_data(sample):
        print("SAMPLE : " , sample)
        try:
            msg_manager = MessageManager.get_instance()
            req_body = {
                        "uuid": sample["uuid"],
                        "environment" : sample["environment"]
                    }
            print("[DEBUG] Sto per mandare : " , req_body)
            msg_manager.send_data(req_body)
            req_body = {
                        "uuid": sample["uuid"],
                        "calendar" : sample["activity"]
                    }
            print("[DEBUG] Sto per mandare : " , req_body)
            msg_manager.send_data(req_body)
            req_body = {
                        "uuid": sample["uuid"],
                        "pressure_detected" : sample["label"]
                    }
            print("[DEBUG] Sto per mandare : " , req_body)
            msg_manager.send_data(req_body)
            req_body = {
                        "uuid": sample["uuid"],
                        "time_series" : sample["ts"]
                    }
            print("[DEBUG] Sto per mandare : " , req_body)
            msg_manager.send_data(req_body)
        except Exception as e:
            raise e


    @staticmethod
    def check_is_empty(data):
        empty = True
        for activity in Dataset.ACTIVITY:
            if len(data[activity]) > 0:
                empty = False
        return empty

    @staticmethod
    def send_ideal_data(interval):
        all_data = Db.get_instance().get_all()
        elaborated_data = Dataset.elaborate_data(all_data)
        print("LEN elb data shopping " , len(elaborated_data["shopping"]))
        print("LEN elb data gaming " , len(elaborated_data["gaming"]))
        print("LEN elb data sport " , len(elaborated_data["sport"]))
        print("LEN elb data cooking " , len(elaborated_data["cooking"]))
        max_len = max(len(elaborated_data["shopping"]),
            len(elaborated_data["gaming"]),
            len(elaborated_data["sport"]),
            len(elaborated_data["cooking"]))
        counter = 0
        for i in range(0 , max_len):
            for activity in Dataset.ACTIVITY:
                if (not(Dataset.check_is_empty(elaborated_data)) and len(elaborated_data[activity]) > 0):
                    sample = elaborated_data[activity][0]
                    try:
                        time.sleep(interval)
                        Dataset.send_data(sample)
                        counter += 1
                    except Exception as e:
                        raise e
                    elaborated_data[activity].pop(0)
        print("[INFO] All samples sended, coounter " , counter)

    @staticmethod
    def send_real_data(interval, prob):
        all_data = Db.get_instance().get_all()
        for data in all_data:
            uuid = data[0]
            label = data[1]
            environment = data[3]
            activity = data[5]
            ts = [value for value in data[7:]]

            sample = {
                "uuid": uuid,
                "environment": environment,
                "label": label,
                "activity": activity,
                "ts" : ts,
            }

            if random.random() < prob:
                random_int = random.randint(1, 4)
                if random_int == 1:
                    key = "environment"
                elif random_int == 2:
                    key = "label"
                elif random_int == 3:
                    key = "activity"
                elif random_int == 4:
                    key = "ts"
                sample[key] = None
            try:
                time.sleep(interval)
                Dataset.send_data(sample)
            except Exception as e:
                raise e
        print("[INFO] All samples sended")
    
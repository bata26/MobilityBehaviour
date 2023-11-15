import sqlite3 
import os
from dotenv import load_dotenv

load_dotenv()

class Db:
    __instance = None

    @staticmethod
    def getInstance():
        if Db.__instance == None:
            Db()
        return Db.__instance
    
    def __init__(self):
        Db.__instance = sqlite3.connect(os.getenv("DB_NAME"))
    
    @staticmethod
    def createTable(tableName , creationString):
        connection = Db.getInstance()
        try:
            connection.cursor().execute(creationString)
            print(f"TABLE {tableName} CORRECTLY CREATED")
            return True
        except Exception as e:
            print(f"Impossibile creare la tabella {tableName}, ERROR: {str(e)}")
        return False
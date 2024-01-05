import os

import json
import sqlite3

class Db:

    _instance = None
    DB_NAME = "input.db"


    def __init__(self):
        os.remove(self.DB_NAME)
        self._connection = sqlite3.connect(self.DB_NAME)

    def get_connection(self):
        return self._connection
    
    @staticmethod
    def get_instance():
        if Db._instance is None:
            Db._instance = Db()
        return Db._instance
    
    def get_all(self):
        cursor = self._connection.cursor()

        cursor.execute("""
                       SELECT * 
                       FROM labels
                       INNER JOIN environment ON labels.uuid = environment.uuid
                       INNER JOIN calendar ON labels.uuid = calendar.uuid
                       INNER JOIN smartShoeSensors ON labels.uuid = smartShoeSensors.uuid
                       
                       """)
        res = cursor.fetchall()
        return res

from utils.json_reader import JsonReader
import pandas as pd
class Report:

    def __init__(self, data):
        self._data = data

    def generate_csv(self, file_path):
        df = pd.DataFrame(self._data)
        df.to_csv(file_path)

    def generate_json(self, file_path):
        JsonReader.write_json_file(file_path , self._data)

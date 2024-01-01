import json

class JsonReader:

    @staticmethod
    def read_json_file(file_path):
        try:
            file_content = {}
            with open(file_path , "r") as file:
                file_content = json.loads(file.read())
            return True, file_content
        except Exception as e:
            print("[ERROR] Impossible to read file located at " + file_path + " because of " + str(e))
            return False, None

    @staticmethod
    def update_json_file(file_path, key, value):
        try:
            file_content = {}
            with open(file_path , "r") as file:
                file_content = json.loads(file.read())

            file_content[key] = value

            JsonReader.write_json_file(file_path, file_content)
            return True
        except Exception as e:
            print("[ERROR] Impossible to update file located at " + file_path + " because of " + str(e))
            return False

    @staticmethod
    def write_json_file(file_path , file_content):
        try:
            with open(file_path , "w") as file:
                json.dump(file_content, file, ensure_ascii=False, indent=4)
                return True
        except Exception as e:
            print("[ERROR] Impossible to write file located at " + file_path + " because of " + str(e))
            return False

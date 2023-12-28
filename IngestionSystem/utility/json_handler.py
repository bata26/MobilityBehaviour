import json
import logging
import os
import jsonschema
import utility

def load_json(self, json_filename: str) -> dict:
        """
        Loads a configuration file written using the JSON format
        :param json_filename: filename of the file to load
        :return: dictionary containing the configuration parameters
        """
        try:
            with open(os.path.join(os.path.abspath('..'), 'data', json_filename)) as f:
                loaded_json = json.load(f)
                return loaded_json

        except FileNotFoundError:
            logging.error(f'Failed to open resources/{json_filename}')
            exit(-1)
            
def validate_json(json_data: dict, schema: dict) -> bool:
    """
    Validate a json object against a json schema.
    :param json_data: json object
    :param schema: json schema
    :return: True if json object is valid, False otherwise.
    """
    try:
        jsonschema.validate(instance=json_data, schema=schema)
    except jsonschema.exceptions.ValidationError as ex:
        logging.error(ex)
        return False
    return True


def validate_json_data_file(json_data: dict, schema_filename: str) -> bool:
    """
    Validate a json object against a json schema in a file.
    :param json_data: json object
    :param schema_filename: path to the json schema relative to the data folder
    :return: True if json object is valid, False otherwise
    """
    schema_path = os.path.join(utility.data_folder, schema_filename)

    with open(schema_path, "r", encoding="UTF-8") as file:
        json_schema = json.load(file)
    return validate_json(json_data, json_schema)


def validate_json_file_file(json_filename: str, schema_filename: str) -> bool:
    """
    Validate a json file against a json schema in a file.
    :param json_filename: file containing the json object
    :param schema_filename: file containing the json schema
    :return: True if json object is valid, False otherwise
    """
    json_path = os.path.join(utility.data_folder, json_filename)
    
    with open(json_path, "r", encoding="UTF-8") as file:
        json_data = json.load(file)
    return validate_json_data_file(json_data, schema_filename)


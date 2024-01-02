import os

project_folder = os.path.realpath(__file__ + "/../../../")
data_folder = os.path.join(project_folder, 'data')
received_data_folder = os.path.join(data_folder, 'received_data')


def get_project_folder() -> str:
    return project_folder


def get_source_folder() -> str:
    return os.path.realpath(get_project_folder() + "/src")


def get_received_data_folder() -> str:
    return received_data_folder


def get_json_schema_folder() -> str:
    return os.path.realpath(get_project_folder() + "/data/json_schema")


def get_tests_folder() -> str:
    return os.path.realpath(get_project_folder() + "/test")

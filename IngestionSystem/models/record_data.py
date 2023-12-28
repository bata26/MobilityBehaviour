class ShoeSensor:
    def __init__(self, uuid: str, time_series: list):
        self.uuid = uuid
        self.time_series = time_series
        

class Environment:
    def __init__(self, uuid: str, environment: str):
        self.uuid = uuid
        self.environment = environment


class Calendar:
    def __init__(self, uuid: str, activity: str):
        self.uuid = uuid
        self.activity = activity

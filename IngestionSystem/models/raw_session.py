class RawSession:
    def __init__(self, uuid: str,
                 label: str,
                 time_series: list,
                 calendar: str,
                 environment: str):
        self.uuid = uuid
        self.pressure_detected = label
        self.time_series = time_series
        self.calendar = calendar
        self.environment = environment
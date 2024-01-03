class PreparedSession:

    def __init__(self , session):
        self.id = session["_id"]
        self.label = session["label"]
        self.maximum_pressure_ts = session["features"]["maximum_pressure_ts"]
        self.minimum_pressure_ts = session["features"]["minimum_pressure_ts"]
        self.median_pressure_ts = session["features"]["median_pressure_ts"]
        self.mean_absolute_deviation_pressure_ts = session["features"]["mean_absolute_deviation_pressure_ts"]
        self.activity = session["features"]["activity_and_small_scatter"]
        self.environment = session["features"]["environment_and_small_scatter"]
        self.human_output = ""

    def to_dataset(self):
        return [{
            "maximum_pressure_ts" : self.maximum_pressure_ts,
            "minimum_pressure_ts" : self.minimum_pressure_ts,
            "median_pressure_ts" : self.median_pressure_ts,
            "mean_absolute_deviation_pressure_ts" : self.mean_absolute_deviation_pressure_ts,
            "activity" : self.activity,
            "environment" : self.environment
        }]

    def add_human_output(self , output):
        self.human_output = output

    def to_json(self):
        return {
            "uuid" : self.id,
            "label" : self.human_output
        }

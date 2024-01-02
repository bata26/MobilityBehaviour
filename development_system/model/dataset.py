class Dataset:
    _instance = {}

    def __init__(self):
        pass

    @staticmethod
    def set_data(data):
        Dataset._instance = {
            "train" : {
                "data": {
                    "maximum_pressure_ts":[],
                    "minimum_pressure_ts":[],
                    "median_pressure_ts":[],
                    "mean_absolute_deviation_pressure_ts":[],
                    "activity":[],
                    "environment":[]
                },
                "labels" : [],
            },
            "validation" : {
                "data": {
                    "maximum_pressure_ts":[],
                    "minimum_pressure_ts":[],
                    "median_pressure_ts":[],
                    "mean_absolute_deviation_pressure_ts":[],
                    "activity":[],
                    "environment":[]
                },
                "labels" : [],
            },
            "test" : {
                "data": {
                    "maximum_pressure_ts":[],
                    "minimum_pressure_ts":[],
                    "median_pressure_ts":[],
                    "mean_absolute_deviation_pressure_ts":[],
                    "activity":[],
                    "environment":[]
                },
                "labels" : [],
            }
        }
        categories = ["train" , "validation" , "test"]
        for category in categories:
            for feature in data[category]["features"]:
                Dataset._instance[category]["labels"].append(feature["label"])
                del feature['label']
                Dataset._instance[category]["data"]["maximum_pressure_ts"].append(feature["maximum_pressure_ts"])
                Dataset._instance[category]["data"]["minimum_pressure_ts"].append(feature["minimum_pressure_ts"])
                Dataset._instance[category]["data"]["median_pressure_ts"].append(feature["median_pressure_ts"])
                Dataset._instance[category]["data"]["mean_absolute_deviation_pressure_ts"].append(feature["mean_absolute_deviation_pressure_ts"])
                Dataset._instance[category]["data"]["activity"].append(feature["activity_and_small_scatter"])
                Dataset._instance[category]["data"]["environment"].append(feature["environment_and_small_scatter"])

    @staticmethod
    def get_data(category):
        return Dataset._instance[category]

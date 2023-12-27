import os
import json

class EvaluationReportGenerator:

    def __init__(self) -> None:
        pass

    def generate_report(self, labels):

        # Counter for the elapsed labels
        labels_counter = 0
        # Counter for the total errors
        error_counter = 0
        # Counter for the consecutive errors
        consecutive_error_counter = 0
        # List to store the previously consecutive errors (memory)
        consecutive_errors = []

        for label in labels:
            labels_counter = labels_counter + 1
            if label['label'] == "Anomalous":
                error_counter = error_counter + 1
                consecutive_error_counter = consecutive_error_counter + 1
            else:
                consecutive_errors.append(consecutive_error_counter)
                consecutive_error_counter = 0

        accuracy = (labels_counter - error_counter) / labels_counter

        # save data just calculated in a dict
        info = dict()
        info['total_errors'] = error_counter
        info['max_consecutive_errors'] = max(consecutive_errors)
        info['accuracy'] = accuracy
        info['evaluation'] = ""

        # Save the report in a json file
        report_path = os.path.join(os.path.abspath('.'), 'data',
                                   'evaluation_report.json')
        try:
            with open(report_path, "w") as file:
                json.dump(info, file, indent=4)
        except Exception as e:
            print(e)
            print('Failure to save evaluation_report.json')
            return False

        print('Evaluation report generated')
        return info

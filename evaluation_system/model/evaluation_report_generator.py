import json
import os
from model.evaluation_report import EvaluationReport


class EvaluationReportGenerator:
    def __init__(self, config):
        self.report = EvaluationReport(config)
        self.labels = None

    def generate_report_json(self):
        report_dict = self.report.to_dict()
        with open(os.path.join(os.path.abspath('.'), 'data', 'report.json'), 'w+', encoding="UTF-8") as file:
            json.dump(report_dict, file, indent=4)
        print("Generated monitoring report json")

    def count_conflicting_labels(self):
        count_conflicting_labels = 0
        tot_labels = 0
        for row in self.labels.index:
            tot_labels += 1
            expert_label = self.labels["expertLabel"][row]
            classifier_label = self.labels["classifierLabel"][row]
            if expert_label != classifier_label:
                count_conflicting_labels += 1
        self.report.conflicting_labels = count_conflicting_labels
        self.report.accuracy = (tot_labels - count_conflicting_labels) / tot_labels
        self.report.compared_labels = tot_labels

    def count_max_consecutive_conflicting_labels(self):
        max_consecutive_conflicting_labels = 0
        consecutive_conflicting_labels = 0
        consecutive = False
        first = True
        for row in self.labels.index:
            expert_label = self.labels["expertLabel"][row]
            classifier_label = self.labels["classifierLabel"][row]
            if expert_label != classifier_label:
                if not consecutive:
                    first = True
                    consecutive_conflicting_labels = 0
                if first or consecutive:
                    consecutive_conflicting_labels += 1
                    consecutive = True
                first = False
            else:
                consecutive = False
            if consecutive_conflicting_labels > max_consecutive_conflicting_labels:
                max_consecutive_conflicting_labels = consecutive_conflicting_labels
        self.report.max_consecutive_conflicting_labels = max_consecutive_conflicting_labels

    def generate_report(self, label_df):
        self.labels = label_df
        if self.labels is not None:
            self.count_conflicting_labels()
            self.count_max_consecutive_conflicting_labels()
        self.generate_report_json()

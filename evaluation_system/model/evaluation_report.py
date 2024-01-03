class EvaluationReport:

    def __init__(self, config):
        self.conflicting_labels = 0
        self.compared_labels = 0
        self.accuracy = 0
        self.max_consecutive_conflicting_labels = 0
        self.max_number_of_tolerated_errors = \
            config.max_number_of_tolerated_errors
        self.max_number_of_consecutive_tolerated_errors = \
            config.max_number_of_consecutive_tolerated_errors

    def to_dict(self):
        return {
            'compared_labels': self.compared_labels,
            'conflicting_labels': self.conflicting_labels,
            'max_consecutive_conflicting_labels': self.max_consecutive_conflicting_labels,
            'accuracy': self.accuracy,
            'max_number_of_tolerated_errors': self.max_number_of_tolerated_errors,
            'max_number_of_consecutive_tolerated_errors':
                self.max_number_of_consecutive_tolerated_errors
        }
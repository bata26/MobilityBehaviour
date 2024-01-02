class ClassifierConfiguration:

    def __init__(self, iterations = 0, hidden_layer_sizes=[]):
        self.iterations_number = iterations
        self.hidden_layer_sizes = hidden_layer_sizes
    def to_dict(self):
        return {
            "max_iter" : self.iterations_number,
            "hidden_layer_sizes" : self.hidden_layer_sizes
        }

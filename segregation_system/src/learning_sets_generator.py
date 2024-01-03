import math
from sklearn.model_selection import train_test_split

class LearningSetsGenerator:

    def __init__(self, config):
        self.segregation_system_config = config

    def generate_learning_sets(self, dataset):
        # Extract features from the prepared sessions in the dataset
        data = []
        for prepared_session in dataset:
            ps = prepared_session['features']
            ps['label'] = prepared_session['label']
            data.append(ps)
        #print(data)


        # train_test_split function can split the dataset only in two part,
        # so it's needed to execute it again to obtain three sets
        train_size = self.segregation_system_config['train_set_size']
        validation_size = self.segregation_system_config['validation_set_size']
        test_size = self.segregation_system_config['test_set_size']

        test_size = math.floor((test_size / (1 - train_size)) * 100) / 100
        validation_size = (100 - test_size * 100) / 100

        train, res = train_test_split(data, train_size=train_size)

        if test_size > validation_size:
            test, validation = train_test_split(res, train_size=test_size)
        else:
            validation, test = train_test_split(res, train_size=validation_size)

        print(f"train_size: {len(train)} validation_size: {len(validation)} test_size: {len(test)}")

        # return the final dataset composed by the splitted dataset
        learning_sets = dict()
        learning_sets['train'] = dict(number_of_samples=len(train), features=train)
        learning_sets['validation']= dict(number_of_samples=len(validation), features=validation)
        learning_sets['test'] = dict(number_of_samples=len(test), features=test)

        return learning_sets
    
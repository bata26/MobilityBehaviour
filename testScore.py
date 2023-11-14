from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from pandas import read_csv
from numpy import ravel
import json


def getAccuration():
    data1 = read_csv("data/hotspotUrbanMobility-1.csv")
    data2 = read_csv("data/hotspotUrbanMobility-2.csv")
    data = data1._append(data2, ignore_index=True)
    data = data.drop("h24", axis=1)
    data = data.loc[data["Anomalous"] < 1]
    data.to_csv("data/preprocessedDataset.csv", index=False)
    data = read_csv("data/preprocessedDataset.csv")
    training_data, testing_data, training_labels, testing_labels = train_test_split(
        data.iloc[:, 4 : len(data.columns)], data.iloc[:, 1]
    )
    # …try to use the default 70-30 split
    mlp = MLPClassifier(random_state=0)
    parameters = {"max_iter": (100, 200, 300)}
    # …try to use all the hyper-params at slide 63
    gs = GridSearchCV(mlp, parameters)
    # ...try PredefinedSplit…
    gs.fit(training_data, ravel(training_labels))
    # ...or try to pick the first runner up config
    config_path = "config/modelConfiguration.json"
    with open(config_path, "w") as f:
        json.dump(gs.best_params_, f)
    with open(config_path, "r") as f:
        params = json.load(f)
    model = MLPClassifier(**params).fit(training_data, ravel(training_labels))
    labels = model.predict(testing_data)
    score = accuracy_score(ravel(testing_labels), labels)
    print(score)
    return score

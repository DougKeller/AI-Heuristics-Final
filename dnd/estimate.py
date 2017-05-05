from sklearn import tree
from sklearn.metrics import confusion_matrix
from pathlib import Path
import sys
import numpy as np
import csv
import os

PATH = 'dnd/difficulty.csv'
TREE = None
CLF = None

class DecisionTreeData(dict):

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

def load_data_from_path(path):
    with open(path) as csv_file:
        data_file = csv.reader(csv_file)
        temp = next(data_file)
        #number of samples is read from first line first word
        n_samples = int(temp[0])

        #number of features available
        n_features = int(temp[1])

        #class names available in first line staring second word
        target_names = np.array(temp[2:])

        #create 2D data array of size n_samples * n_features
        data = np.empty((n_samples, n_features))

        #create an array of size n_samples * n_features
        target = np.empty((n_samples,), dtype=np.int)

        #iterate over remaining data and fill in data and target arrays
        for i, ir in enumerate(data_file):
            data[i] = np.asarray(ir[:-1], dtype=np.float64)
            target[i] = np.asarray(ir[-1], dtype=np.int)


    return DecisionTreeData(
        data=data,
        target=target,
        target_names=target_names,
        feature_names=['player count', 'player level', 'player std', 'monster count', 'mounster level', 'monster std']
    )


def load_dnd_tree():
    return load_data_from_path(PATH)

def test_accuracy():
    test_path = raw_input("Enter the path of the test file: ")
    test_data = load_data_from_path(test_path)

    results = CLF.predict(test_data.data)
    print "Confusion Matrix: \n"
    print confusion_matrix(test_data.target, results)

def test(case):
    prediction = CLF.predict([case])
    return TREE.target_names[prediction][0]

def get_dnd_tree_and_classifer():
    dnd_tree = load_dnd_tree()
    classifier = tree.DecisionTreeClassifier()
    classifier = classifier.fit(dnd_tree.data, dnd_tree.target)

    result = [dnd_tree, classifier]

    return result

if Path("dnd/user_file.csv").is_file():
    PATH = "dnd/user_file.csv"

result = get_dnd_tree_and_classifer()
TREE = result[0]
CLF = result[1]

player_count = int(sys.argv[1])
player_level = float(sys.argv[2])
player_std = float(sys.argv[3])
monster_count = int(sys.argv[4])
monster_level = float(sys.argv[5])
monster_std = float(sys.argv[6])
case = [player_count, player_level, player_std, monster_count, monster_level, monster_std]
result = test(case)

if Path("dnd/user_file.csv").is_file():
    os.remove('dnd/user_file.csv')

print(result)
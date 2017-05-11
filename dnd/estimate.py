from sklearn import tree
from sklearn.metrics import confusion_matrix
from pathlib import Path
import sys
import numpy as np
import csv
import os
import math
import random
import cPickle

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

    def partition(self, num, fold_index):
        fold_size = len(self.data) / 10
        start = num * fold_size
        end = start + fold_size

        if end >= len(self.data):
            end = len(self.data)

        tree_data = self.data[0:start] + self.data[end:-1]
        tree_target = self.target[0:start] + self.target[end:-1]

        test_data = self.data[start:end]
        test_target = self.target[start:end]

        return [tree_data, tree_target, test_data, test_target]


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

        #randomize the data
        grouped_rows = zip(data, target)
        random.shuffle(grouped_rows)
        data, target = zip(*grouped_rows)


    return DecisionTreeData(
        data=data,
        target=target,
        target_names=target_names,
        feature_names=['player count', 'player level', 'monster count', 'mounster level', 'monster std']
    )


def load_dnd_tree():
    return load_data_from_path(PATH)

def test(case):
    prediction = CLF.predict([case])
    return TREE.target_names[prediction][0]

# if Path("dnd/user_file.csv").is_file():
#     PATH = "dnd/user_file.csv"

if sys.argv[1] == 'build':
    tree_of_best_fit = None
    best_accuracy = 0

    for _ in range(100):
        arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        dnd_tree = load_dnd_tree()

        for i in arr:
            res = dnd_tree.partition(i, 10)
            tree_data = res[0]
            tree_target = res[1]
            test_data = res[2]
            test_target = res[3]

            if len(tree_target) == 0 or len(test_target) == 0:
                break

            classifier = tree.DecisionTreeClassifier()
            classifier = classifier.fit(tree_data, tree_target)
            results = classifier.predict(test_data)
            matrix = confusion_matrix(test_target, results)

            num_correct = 0
            total = 0

            for i, row in enumerate(matrix):
                for j, cell in enumerate(row):
                    if i == j:
                        num_correct += cell

                    total += cell

            accuracy = num_correct / float(total)
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                tree_of_best_fit = [dnd_tree, classifier]

    with open('dnd/best_fit.pkl', 'wb') as file:
        cPickle.dump(tree_of_best_fit, file)
    with open('dnd/accuracy.txt', 'w') as file:
        file.write(str(best_accuracy))

elif sys.argv[1] == 'accuracy':
    with open('dnd/accuracy.txt', 'rb') as file:
        print file.read()
else:
    with open('dnd/best_fit.pkl', 'rb') as file:
        result = cPickle.load(file)
        TREE = result[0]
        CLF = result[1]

        player_count = int(sys.argv[1])
        player_level = float(sys.argv[2])
        monster_count = int(sys.argv[3])
        monster_level = float(sys.argv[4])
        monster_std = float(sys.argv[5])
        case = [player_count, player_level, monster_count, monster_level, monster_std]
        result = test(case)

        print(result)
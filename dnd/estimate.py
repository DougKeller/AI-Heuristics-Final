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
        fold_size = len(self.data) / self.folds
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
        feature_names=['level ratio', 'count ratio', 'monster std']
    )


def load_dnd_tree():
    return load_data_from_path(PATH)

def test(case):
    prediction = CLF.predict([case])
    return TREE.target_names[prediction][0]

# if Path("dnd/user_file.csv").is_file():
#     PATH = "dnd/user_file.csv"

if sys.argv[1] == 'build':
    overall_accuracy = []

    best_tree = None
    best_accuracy = 0

    for _ in range(100):
        dnd_tree = load_dnd_tree()
        dnd_tree.folds = 10

        local_accuracy = []

        for i in range(dnd_tree.folds):
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
            overall_accuracy.append(accuracy)
            local_accuracy.append(accuracy)

        average_accuracy = sum(local_accuracy) / len(local_accuracy)
        if average_accuracy > best_accuracy:
            best_tree = dnd_tree
            best_accuracy = average_accuracy

    with open('dnd/decision_tree.pkl', 'wb') as file:
        # Generate the full tree and save it
        classifier = tree.DecisionTreeClassifier()
        classifier = classifier.fit(dnd_tree.data, dnd_tree.target)

        decision_tree = [dnd_tree, classifier]
        cPickle.dump(decision_tree, file)
    with open('dnd/accuracy.txt', 'w') as file:
        file.write(str(best_accuracy))

elif sys.argv[1] == 'accuracy':
    with open('dnd/accuracy.txt', 'rb') as file:
        print file.read()
else:
    with open('dnd/decision_tree.pkl', 'rb') as file:
        result = cPickle.load(file)
        TREE = result[0]
        CLF = result[1]

        level_ratio = float(sys.argv[1])
        count_ratio = float(sys.argv[2])
        monster_std = float(sys.argv[3])

        case = [count_ratio, level_ratio, monster_std]
        result = test(case)

        print(result)
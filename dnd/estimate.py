from sklearn import tree
from sklearn.metrics import confusion_matrix
import sys
import numpy as np
import csv
import cPickle
import os

PATH = 'dnd/difficulty.csv'
IRIS = None
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
    #change below csv file path
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


    return DecisionTreeData(data=data, target=target,
                 target_names=target_names,
                 feature_names=['sepal length (cm)', 'sepal width (cm)',
                                'petal length (cm)', 'petal width (cm)'])


def load_iris():
    return load_data_from_path(PATH)

def test_accuracy():
    test_path = raw_input("Enter the path of the test file: ")
    test_data = load_data_from_path(test_path)

    results = CLF.predict(test_data.data)
    print "Confusion Matrix: \n"
    print confusion_matrix(test_data.target, results)

def test(case):
    prediction = CLF.predict([case])
    return IRIS.target_names[prediction][0]

def get_iris_and_classifer():
    file, extension = os.path.splitext(PATH)
    existing = extension == '.pkl'

    if existing:
        with open(PATH, 'rb') as file:
            return cPickle.load(file)

    else:
        iris = load_iris()
        classifier = tree.DecisionTreeClassifier()
        classifier = classifier.fit(iris.data, iris.target)

        with open(PATH + '.dot', 'w') as file:
            f = tree.export_graphviz(classifier, out_file=file)

        # Save the generated tree
        result = [iris, classifier]
        with open(PATH + '.pkl', 'wb') as file:
            cPickle.dump(result, file)

        return result

result = get_iris_and_classifer()
IRIS = result[0]
CLF = result[1]

sepal_length = float(sys.argv[1])
sepal_width = float(sys.argv[2])
petal_length = float(sys.argv[3])
petal_width = float(sys.argv[4])
case = [sepal_length, sepal_width, petal_length, petal_width]
result = test(case)
print(result)
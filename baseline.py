__author__ = 'fangy'

import pdb

from sklearn.feature_extraction.text import HashingVectorizer, CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

import utils


def load_data(xml_file, vectorizer):

    texts, labels = [], []
    for values, label in utils.read_corpus(xml_file):
        texts.append(values[0])
        labels.append(label)
    feas = vectorizer.fit_transform(texts)
    # pdb.set_trace()
    labeled_data = {"data": feas, "label": labels}

    print "the feature of data:", feas.shape

    return labeled_data


def classify_by_nb(train_data, test_data):

    clf = MultinomialNB(alpha=0.01)
    clf.fit(train_data["data"], train_data["label"])
    label_pred = clf.predict(test_data["data"])
    acc = accuracy_score(test_data["label"], label_pred)

    print "NB:\n", xml_train_file, "\n", xml_test_file, "\n", acc

def classify_by_knn(train_data, test_data):

    knnclf = KNeighborsClassifier()
    knnclf.fit(train_data["data"], train_data["label"])
    label_pred = knnclf.predict(test_data["data"])
    acc = accuracy_score(test_data["label"], label_pred)

    print "KNN:\n", xml_train_file, "\n", xml_test_file, "\n", acc

def classify_by_svm(train_data, test_data):

    svclf = SVC(kernel='linear')
    svclf.fit(train_data["data"], train_data["label"])
    label_pred = svclf.predict(test_data["data"])
    acc = accuracy_score(test_data["label"], label_pred)

    print "SVM:\n", xml_train_file, "\n", xml_test_file, "\n", acc

if __name__ == "__main__":

    xml_train_file = '/Users/fangy/data/cl14-unprocessed/cn/books/train.review'
    xml_test_file = '/Users/fangy/data/cl14-unprocessed/cn/books/test.review'

    # vectorizer = HashingVectorizer(stop_words='english', non_negative=True,
    #                                n_features=20000, binary=True)
    vectorizer = CountVectorizer(max_df=0.5)

    train_data = load_data(xml_train_file, vectorizer)

    vectorizer = CountVectorizer(vocabulary=vectorizer.vocabulary_,
                                 max_df=0.5)

    test_data = load_data(xml_test_file, vectorizer)

    classify_by_nb(train_data, test_data)
    classify_by_knn(train_data, test_data)
    classify_by_svm(train_data, test_data)

"""
    Contain some kind of classifier
"""
from adaboost import AdaClassifier

class OpiClassifier(AdaClassifier):
    """
    """
    def __init__(self, feature):
        AdaClassifier.__init__(self, '+ '+feature)

        self.feature = feature

    def classify(self, sample):
        
        if self.feature in sample:
            return 1
        else: return -1

class NopiClassifier(AdaClassifier):
    """
    """
    def __init__(self, feature):
        AdaClassifier.__init__(self, '- '+feature)

        self.feature = feature

    def classify(self, sample):
        
        if self.feature not in sample:
            return 1
        else: return -1

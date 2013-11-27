
import sys,math

class AdaBoostV3:
    """AdaBoostV3"""
    def __init__(self):
        pass

    def __init__(self, sampleSet=[]):

        if len(sampleSet) > 0:
            self.sampleSet = sampleSet
            self.N = len(self.sampleSet)
            self.weights = [1/self.N for i in range(0, self.N)]
        self.classifiers = []
        self.alphas = []
        self.resClassifiers = []

    def addClassifier(self, adaClassifier):
        self.classifiers.append(adaClassifier)

    def addResClassifier(self, classifier, alpha):
        """
        add classifier to AdaBoostV3 model
        """
        self.resClassifiers.append(classifier)
        self.alphas.append(alpha)

    def findMaxClassifier(self):
        errors = [0 for i in range(0, len(self.classifiers))]
        for ci in range(0, len(self.classifiers)):
            # csfier = self.classifiers[ci]
            for si in range(0, len(self.sampleSet)):
                if self.classifiers[ci].classify(self.sampleSet[si]) != self.sampleSet[si][0]:
                    errors[ci] += self.weights[si]
        # print(errors)
        maxBeta, maxCi = 0, 0
        for ei in range(0, len(errors)):
            beta = abs(0.5 - errors[ei])
            if beta > maxBeta:
                maxBeta = beta
                maxCi = ei
        self.resClassifiers.append(self.classifiers[maxCi])
        self.alphas.append(0.5*math.log(1/errors[ei] - 1))
        del self.classifiers[maxCi]

        return maxBeta

    def updateWeights(self):
        # newClassifier = self.resClassifiers[-1]
        newAlpha = self.alphas[-1]
        factor = 0
        for wi in range(0, len(self.weights)):
            self.weights[wi] *= math.exp(
                -newAlpha * self.sampleSet[wi][0] * self.predict(self.sampleSet[wi])) 
            factor += self.weights[wi]

        for wi in range(0, len(self.weights)):
            self.weights[wi] /= factor

    def trainingByBeta(self, beta):

        maxBeta = float('inf')
        print('Training... Max beta list below:')

        while maxBeta > beta and len(self.classifiers) > 0:
            maxBeta = self.findMaxClassifier()
            self.updateWeights()
            print(maxBeta)
            
        print('Done.')
        return maxBeta

    def trainingByNum(self, num):

        if num > len(self.classifiers):
            num = len(self.classifiers)
        classifierCount = 0
        minDiff = float('inf')
        while classifierCount < num:
            minDiff = self.findMaxClassifier()
            self.updateWeights()
            # print(minDiff)
            classifierCount += 1
        # print(self.alphas)
        return minDiff

    def predict(self, sample):

        hs = self.predictForValue(sample)

        if hs <= 0:
            return -1
        else:
            return 1

    def predictForValue(self, sample):

        hs = 0
        for ci in range(0, len(self.resClassifiers)):
            hs += self.alphas[ci] * self.resClassifiers[ci].classify(sample)

        return hs

    def formatStr(self):
        """
        Reture the format string of training result like:
            EN:0.324
            2-IAO:0.244
        """
        fstr = ''
        for opi in range(0, len(self.resClassifiers)):
            fstr += self.resClassifiers[opi].getNote() + \
            ':' + str(self.alphas[opi]) + '\n'
        return fstr

        

if __name__ == '__main__':
    
    if len(sys.argv) != 3: 
        sys.exit(2)


    # funcList = []
    # i_List = []
    # for i in range(0, 3):

    #     i_List.append(i)
    #     def printI():
    #         print(i_List[i], end = ',')
    #     funcList.append(printI)
    
    # print(funcList[0]() )
    # print(funcList[1]() )
    # print(funcList[2]() )
    # print(i_List)


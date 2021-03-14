import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer
from PandioML import PandioML
from PandioFunctionInterface import PandioFunctionInterface


class Test(PandioFunctionInterface):
    model = None

    def __init__(self, model):
        self.model = model
        self.vectorizer = HashingVectorizer(n_features=20)

    def label_extraction(self, input):
        if 'spam' in input:
            return np.array([input['spam']])

        return None

    def feature_extraction(self, input):
        if 'spam' in input:
            length = len(input) + 21
        else:
            length = len(input) + 22

        data = np.zeros([1, length])

        index = 0
        for key in input:
            if key != 'spam':
                if key == 'email':
                    hash_list = self.vectorizer.transform([input[key]]).toarray()
                    for h in range(len(hash_list[0])):
                        data[0, index] = hash_list[0][h]
                        index += 1
                elif key == 'ip':
                    ip_list = input[key].split(".")[:4]
                    for h in range(len(ip_list)):
                        data[0, index] = ip_list[h]
                        index += 1
                else:
                    data[0, index] = input[key]
                    index += 1

        return data

    def fit(self, features, labels):
        self.model.partial_fit(features, labels)

    def predict(self, features):
        return self.model.predict(features)


arr = {
    'email': 'steph_l_jacobs@yahoo.com',
    'ip': '182.54.239.221',
    'timestamp': 582055077,
    'weekday': 5,
    'weekend': 1.0,
    'month': 6,
    'day': 11,
    'hour': 17
}

f = Test(model=PandioML(token='test').models.naive_bayes())
print(f.feature_extraction(arr))
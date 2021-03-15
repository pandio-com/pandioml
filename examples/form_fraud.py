import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import HashingVectorizer
from pandioml.model import NaiveBayes
from pandioml.function import FunctionInterface
from pandioml.dataset import FormSubmissionGenerator
import matplotlib.pyplot as plt
import pickle
from os import path


class FormFraud(FunctionInterface):
    model = None

    def __init__(self, model):
        self.model = model
        self.vectorizer = HashingVectorizer(n_features=20)

    def label_extraction(self, input):
        if 'yahoo' in input['email'] or 'hotmail' in input['email']:
            return np.array([1])
        else:
            return np.array([0])

    def _label_extraction(self, input):
        ip_list = input['ip'].split(".")[:4]
        if int(ip_list[0]) == 82:
            return np.array([1])
        else:
            return np.array([0])

    def feature_extraction(self, input):
        length = len(input) + 27

        data = np.zeros([1, length])

        index = 0
        for key in input:
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
            elif key == 'timestamp':
                data[0, index] = input[key]
                index += 1
                timestamp_formatted = pd.to_datetime(input[key], unit='s')
                data[0, index] = timestamp_formatted.dayofweek
                index += 1
                data[0, index] = 1 if (timestamp_formatted.dayofweek // 5 == 1) else 0
                index += 1
                data[0, index] = timestamp_formatted.month
                index += 1
                data[0, index] = timestamp_formatted.day
                index += 1
                data[0, index] = timestamp_formatted.hour
                index += 1

        return data

    def fit(self, features, labels):
        self.model.partial_fit(features, labels)

    def predict(self, features):
        return self.model.predict(features)

model_file_name = "form_fraud_example.model"

if path.exists(model_file_name):
    file = open(model_file_name, 'rb')
    model = pickle.load(file)
    file.close()
else:
    model = NaiveBayes()

nb_iters = 10000
time = [i for i in range(1, nb_iters)]
correctness_dist = []
f = FormFraud(model=model)
generator = FormSubmissionGenerator(0, nb_iters)

index = 0
while generator.has_more_samples():
    for event in generator.next_sample():
        index += 1
        labels = f.label_extraction(event)
        features = f.feature_extraction(event)
        f.fit(features, labels)
        p = f.predict(features)
        if p == labels:
            correctness_dist.append(1)
        else:
            correctness_dist.append(0)

file = open(model_file_name, 'wb')
pickle.dump(f.model, file)
file.close()

accuracy = [sum(correctness_dist[:i])/len(correctness_dist[:i]) for i in range(1, nb_iters)]
plt.plot(time, accuracy)
plt.show()

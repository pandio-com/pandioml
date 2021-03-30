from pandioml.model import NaiveBayes
from pandioml.data import FormSubmissionGenerator
import matplotlib.pyplot as plt
import pickle
from os import path
pm = __import__('function')
Fnc = pm.Fnc

model_file_name = "example.model"

if path.exists(model_file_name):
    file = open(model_file_name, 'rb')
    model = pickle.load(file)
    file.close()
else:
    model = NaiveBayes()

nb_iters = 1000
time = [i for i in range(1, nb_iters)]
correctness_dist = []
f = Fnc(model=model)
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

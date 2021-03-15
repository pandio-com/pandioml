from pandioml.model import NaiveBayes
from pandioml.function import FunctionInterface
from pandioml.dataset import FormSubmissionGenerator


class FormFraud(FunctionInterface):
    model = None

    def __init__(self, model):
        self.model = model

    def label_extraction(self, input):
        return None

    def feature_extraction(self, input):
        return None

    def fit(self, features, labels):
        return None

    def predict(self, features):
        return None


i = FormFraud(NaiveBayes())

print(i)

generator = FormSubmissionGenerator()

while generator.has_more_samples():
    input = generator.next_sample()
    print(input)

from pandioml.function import FunctionBase
from pandioml.core import Pipeline, Pipelines
from pandioml.core.artifacts import artifact
from pandioml.model import LogisticRegression
from pandioml.model import StandardScaler
from pandioml.data.record import Float, Boolean, Record
from pandioml.metrics import Accuracy, Precision, Recall, ConfusionMatrix


class Output(Record):
    Time = Float()
    prediction = Boolean()


class Function(FunctionBase):
    model = artifact.add('LogisticRegression_model', LogisticRegression())
    scaler = StandardScaler()
    accuracy = Accuracy()
    precision = Precision()
    recall = Recall()
    confusion_matrix = ConfusionMatrix()

    def feature_extraction(self, result={}):
        # Remove Class from features
        result['features'] = {k: v for k, v in self.input.__dict__.items() if 'Class' != k and k[0] != '_'}

        return result

    def scale(self, result={}):
        result['features'] = self.scaler.learn_one(result['features']).transform_one(result['features'])
        return result

    def label_extraction(self, result={}):
        result['labels'] = self.input.Class

        return result

    def done(self, result={}):
        self.accuracy = artifact.add('Accuracy_Metric', self.accuracy.update(result['labels'], result['prediction']))
        self.precision = artifact.add('Precision_Metric', self.precision.update(result['labels'], result['prediction']))
        self.recall = artifact.add('Recall_Metric', self.recall.update(result['labels'], result['prediction']))
        self.confusion_matrix = artifact.add('Confusion_Matrix_Metric', self.confusion_matrix.update(result['labels'],
                                                                                                     result['prediction']))
        print(self.accuracy)
        print(self.precision)
        print(self.recall)
        print(self.confusion_matrix)
        return Output(Time=self.input.Time, prediction=result['prediction'])

    def pipelines(self, *args, **kwargs):
        return Pipelines().add(
            'inference',
            Pipeline(*args, **kwargs)
                .then(self.feature_extraction)
                .then(self.scale)
                .then(self.label_extraction)
                .then(self.fit)
                .final(self.predict)
                .done(self.done)
                .catch(self.error)
        )

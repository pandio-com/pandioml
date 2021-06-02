from pandioml.function import FunctionBase
from pandioml.core import Pipeline, Pipelines
from pandioml.core.artifacts import artifact
from pandioml.model import LogisticRegression
from pandioml.model import StandardScaler
from pandioml.data.record import Float, Boolean, Record, Integer, JsonSchema
from pandioml.metrics import Accuracy, Precision, Recall, ConfusionMatrix


class Transaction(Record):
    Time = Float()
    V1 = Float()
    V2 = Float()
    V3 = Float()
    V4 = Float()
    V5 = Float()
    V6 = Float()
    V7 = Float()
    V8 = Float()
    V9 = Float()
    V10 = Float()
    V11 = Float()
    V12 = Float()
    V13 = Float()
    V14 = Float()
    V15 = Float()
    V16 = Float()
    V17 = Float()
    V18 = Float()
    V19 = Float()
    V20 = Float()
    V21 = Float()
    V22 = Float()
    V23 = Float()
    V24 = Float()
    V25 = Float()
    V26 = Float()
    V27 = Float()
    V28 = Float()
    Amount = Float()
    Class = Integer()


class Output(Record):
    Time = Float()
    prediction = Boolean()


class Function(FunctionBase):
    model = artifact.add('LogisticRegression_model', LogisticRegression())
    input_schema = JsonSchema(Transaction)
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

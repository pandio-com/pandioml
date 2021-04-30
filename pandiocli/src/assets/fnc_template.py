from pandioml.function import FunctionBase
from pandioml.core import Pipeline, Pipelines
from pandioml.core.artifacts import artifact
from pandioml.model import GaussianNB


class Fnc(FunctionBase):
    model = artifact.add('GaussianNB_model', GaussianNB())

    def feature_extraction(self, result={}):
        result['features'] = {'feature_one': 0, 'feature_two': 1}

        return result

    def label_extraction(self, result={}):
        result['labels'] = 0

        return result

    def done(self, result={}):
        return result['prediction']

    def pipelines(self, *args, **kwargs):
        return Pipelines().add(
            'inference',
            Pipeline(*args, **kwargs)
                .then(self.feature_extraction)
                .then(self.label_extraction)
                .then(self.fit)
                .final(self.predict)
                .done(self.done)
                .catch(self.error)
        )

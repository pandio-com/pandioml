from pandioml.function import FunctionBase
from pandioml.core import Pipeline, Pipelines
import numpy as np
from pandioml.core.artifacts import artifact
from pandioml.model import GaussianNB


class Fnc(FunctionBase):
    model = artifact.add('GaussianNB_model', GaussianNB())
    input_schema = None
    output_schema = None

    def feature_extraction(self, result={}):
        result['features'] = np.array([[1, 1]])

        return result

    def label_extraction(self, result={}):
        result['labels'] = np.array([0])

        return result

    def pipelines(self, *args, **kwargs):
        return Pipelines().add(
            'inference',
            Pipeline(*args, **kwargs)
                .then(self.feature_extraction)
                .then(self.label_extraction)
                .then(self.fit)
                .final(self.predict)
                .done(self.output)
                .catch(self.error)
        )

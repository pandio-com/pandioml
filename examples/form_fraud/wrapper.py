import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from pandioml.function import Function
from pandioml.core import Pipelines
import fnc as pm


class Wrapper(Function):
    id = None
    fnc = None
    output = None

    def __init__(self):
        pass

    def process(self, input, context, id=None):
        input = pm.Fnc.schema.decode(input)
        self.fnc = pm.Fnc(id, input, context)
        print(self.fnc.model._observed_class_distribution)
        try:
            self.fnc.startup()
        except Exception as e:
            raise Exception(f"Could not execute startup method: {e}")

        try:
            p = self.fnc.pipelines()
        except Exception as e:
            raise Exception(f"Could not build pipelines: {e}")

        if isinstance(p, Pipelines) is False:
            raise Exception(f"Method pipelines should return a Pipelines object!")

        try:
            self.output = p.go(context.get_user_config_value('pipeline'))
        except Exception as e:
            raise Exception(f"Could not execute pipeline: {e}")

        if self.fnc.id is not None:
            context.incr_counter(self.fnc.id, 1)

            count = context.get_counter(self.fnc.id)

            if count > 0 and count % 1000 == 0:
                self.fnc.sync_models(context)

        input = pm.Fnc.schema.encode(input).decode('UTF-8')

        return input

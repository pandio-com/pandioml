from pandioml.function import Function
from pandioml.core import Pipelines
pm = __import__('function')


class Wrapper(Function):
    id = None
    fnc = None
    output = None

    def __init__(self, id):
        self.id = id

    def process(self, input, context):
        self.fnc = pm.Fnc(self.id, input, context)
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

        context.incr_counter(self.fnc.id, 1)

        count = context.get_counter(self.fnc.id)

        if count > 0 and count % 1000 == 0:
            self.fnc.sync_models(context)

        return input

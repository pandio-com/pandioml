import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from pandioml.function import Function
from pandioml.core import Pipelines
import fnc as pm
import config
from pandioml.core import interact

class Wrapper(Function):
    id = None
    fnc = None
    output = None

    def __init__(self):
        pass

    def process(self, input, context, id=None):
        self.fnc = pm.Fnc(id, pm.Fnc.input_schema.decode(input), context)
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

        if 'OUTPUT_TOPICS' in config.pandio:
            for output_topic in config.pandio['OUTPUT_TOPICS']:
                context.publish(output_topic, pm.Fnc.output_schema.encode(self.fnc.output).decode('UTF-8'))

        if self.fnc.id is not None:
            context.incr_counter(self.fnc.id, 1)

            count = context.get_counter(self.fnc.id)

            if count > 0 and count % 1000 == 0:
                self.fnc.sync_models(context)

        return input

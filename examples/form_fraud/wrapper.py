import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from pandioml.function import Function
from pandioml.core import Pipelines
import fnc as pm
import config
from pandioml.core.artifacts import artifact
import time

artifact.set_storage_location(config.pandio['ARTIFACT_STORAGE'])


class Wrapper(Function):
    fnc = None
    output = None

    def __init__(self):
        artifact.add('runtime_settings', {'config.pandio': config.pandio, 'sys.version': sys.version,
                                          'timestamp': time.strftime("%Y%m%d-%H%M%S")})

    def process(self, input, context):
        self.fnc = pm.Fnc(pm.Fnc.input_schema.decode(input), context, config)
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
                if self.fnc.output is not None:
                    context.publish(output_topic, pm.Fnc.output_schema.encode(self.fnc.output).decode('UTF-8'))
                else:
                    print("Warning, output variable is empty, should be defined in self.fnc.done method.")

        if artifact.get_name_id() is not None:
            context.incr_counter(artifact.get_name_id(), 1)

            count = context.get_counter(artifact.get_name_id())

            if count > 0 and count % 1000 == 0:
                #self.fnc.sync_models(context)
                if artifact.get_pipeline_id() is not None:
                    artifact.save(checkpoint=True)

        return input

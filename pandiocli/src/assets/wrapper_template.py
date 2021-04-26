import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from pandioml.function import Function
from pandioml.core import Pipelines
import fnc as pm
import config
from pandioml.core.artifacts import artifact
import time
from pandioml.data.record import JsonSchema

artifact.set_storage_location(config.pandio['ARTIFACT_STORAGE'])


class Wrapper(Function):
    fnc = None
    result = None
    input_schema = None

    def __init__(self, dataset_name=None):
        artifact.add('runtime_settings', {'config.pandio': config.pandio, 'sys.version': sys.version,
                                          'timestamp': time.strftime("%Y%m%d-%H%M%S")})
        if dataset_name is not None:
            self.input_schema = getattr(__import__('pandioml.data', fromlist=[dataset_name]), dataset_name).schema()

    def process(self, input, context):
        self.fnc = pm.Fnc(self.input_schema.decode(input), context, config)
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
            output = p.go(context.get_user_config_value('pipeline'), self.fnc)
            self.result = self.fnc.get_result()
        except Exception as e:
            raise Exception(f"Could not execute pipeline: {e}")

        if 'OUTPUT_TOPICS' in config.pandio:
            for output_topic in config.pandio['OUTPUT_TOPICS']:
                if output is not None:
                    context.publish(output_topic, JsonSchema(getattr(pm, output[context.get_user_config_value('pipeline')].schema()['name'])).encode(output[context.get_user_config_value('pipeline')]).decode('UTF-8'))
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

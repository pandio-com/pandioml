import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from pandioml.function import Function
import dataset as _dataset
import config


class Wrapper(Function):
    _dataset = None

    def __init__(self):
        pass

    def process(self, input, context):
        if 'OUTPUT_TOPICS' in config.pandio:
            d = _dataset.Dataset()
            while True:
                try:
                    for output_topic in config.pandio['OUTPUT_TOPICS']:
                        context.publish(output_topic, _dataset.Dataset.schema().encode(d.next()).decode('UTF-8'))
                except StopIteration:
                    break
        else:
            print('No output topics defined.')

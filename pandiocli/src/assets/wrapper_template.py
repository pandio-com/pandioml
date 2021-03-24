import signal
from pandioml.function import Function
pm = __import__('function')
fnc = pm.Fnc()

class Wrapper(Function):
    def __init__(self):
        try:
            fnc.startup()
        except:
            logger.error("Could not execute startup method.")
            raise Exception("Could not execute startup method.")

    def process(self, input, context):
        logger = context.get_logger()

        arr = {}
        arr['input'] = input

        try:
            labels = fnc.label_extraction(input)
        except:
            logger.error("Could not extract labels.")
            raise Exception("Could not extract labels.")

        try:
            features = fnc.feature_extraction(input)
        except:
            logger.error("Could not extract features.")
            raise Exception("Could not extract features.")

        try:
            if labels is not None:
                fnc.fit(features, labels)
        except:
            logger.error("Could not fit model from features and labels.")
            raise Exception("Could not fit model from features and labels.")

        try:
            if features is not None:
                arr['output'] = fnc.predict(features)
        except:
            logger.error("Could not predict with extracted features.")
            raise Exception("Could not predict with extracted features.")

        return arr


signal.signal(signal.SIGINT, fnc.shutdown)
signal.signal(signal.SIGTERM, fnc.shutdown)

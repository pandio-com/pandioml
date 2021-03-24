from pandioml.function import Function
pm = __import__('function')


class Wrapper(Function):
    fnc = None

    def __init__(self):
        self.fnc = pm.Fnc()
        try:
            self.fnc.startup()
        except:
            raise Exception("Could not execute startup method.")

    def process(self, input, context):
        logger = context.get_logger()

        arr = {}
        arr['input'] = input

        try:
            labels = self.fnc.label_extraction(input)
        except:
            logger.error("Could not extract labels.")
            raise Exception("Could not extract labels.")

        try:
            features = self.fnc.feature_extraction(input)
        except:
            logger.error("Could not extract features.")
            raise Exception("Could not extract features.")

        try:
            if labels is not None:
                self.fnc.fit(features, labels)
        except:
            logger.error("Could not fit model from features and labels.")
            raise Exception("Could not fit model from features and labels.")

        try:
            if features is not None:
                arr['output'] = self.fnc.predict(features)
        except:
            logger.error("Could not predict with extracted features.")
            raise Exception("Could not predict with extracted features.")

        return arr

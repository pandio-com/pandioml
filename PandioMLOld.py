import skmultiflow
import pulsar


class PandioML():
    models = None
    host = ''
    token = ''
    port = None
    pandio_client = None

    def __init__(self, token, host='localhost', port=6680):
        class Models():
            def __init__(self):
                pass

            @staticmethod
            def naive_bayes():
                return skmultiflow.bayes.NaiveBayes()

        self.models = Models()
        self.host = host
        self.token = token
        self.port = port
        self.pandio_client = pulsar.Client(f"pulsar://{self.host}:{self.port}")

    def list_models(self):
        """List models available"""
    def get_model(self, arn):
        """Retrieve requested model"""
    def save_model(self, arn, model):
        """Save model"""

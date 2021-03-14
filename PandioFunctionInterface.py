from abc import abstractmethod, ABCMeta, abstractproperty


class PandioFunctionInterface(object, metaclass=ABCMeta):
    """Interface for Pandio Function"""
    model = abstractproperty()

    @abstractmethod
    def feature_extraction(self, input):
        """Process input message"""
        raise NotImplementedError

    @abstractmethod
    def label_extraction(self, input):
        """Process input message"""
        raise NotImplementedError

    @abstractmethod
    def predict(self, features):
        """Process input message"""
        raise NotImplementedError

    @abstractmethod
    def fit(self, features, labels):
        """Process input message"""
        raise NotImplementedError

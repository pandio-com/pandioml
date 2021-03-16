from abc import abstractmethod, ABCMeta, abstractproperty


class FunctionInterface(object, metaclass=ABCMeta):
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

from abc import ABCMeta, abstractmethod


class Stream(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def next(self):
        pass

from abc import ABCMeta, abstractmethod, abstractproperty
import re
import inspect


class Stream(object, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def dataset(self):
        raise NotImplementedError

    @abstractmethod
    def next(self):
        raise NotImplementedError

    @abstractmethod
    def schema(self):
        raise NotImplementedError

    @property
    def desc(self):
        """Return the description from the docstring."""
        desc = re.split(pattern=r"\w+\n\s{4}\-{3,}", string=self.__doc__, maxsplit=0)[0]
        return inspect.cleandoc(desc)

    def __repr__(self):
        out = f"{self.desc}"
        if hasattr(self, 'data'):
            out += "\n\n" + self.data.__repr__()

        return out

    def __iter__(self):
        return self.dataset

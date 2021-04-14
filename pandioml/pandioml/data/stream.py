from abc import ABCMeta, abstractmethod
import re
import inspect


class Stream(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def next(self):
        pass

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

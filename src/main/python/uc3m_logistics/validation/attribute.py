# pylint: disable=missing-module-docstring
from abc import ABC, abstractmethod


class Attribute(ABC):
    """Abstract class attribute"""

    def __init__(self, value):
        self.validate(value)
        self.__value = value

    @abstractmethod
    # pylint: disable=missing-function-docstring
    def validate(self, value):
        pass

    @property
    # pylint: disable=missing-function-docstring
    def value(self):
        return self.__value

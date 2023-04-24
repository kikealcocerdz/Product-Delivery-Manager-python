from abc import ABC, abstractmethod


class Attribute(ABC):

    def __init__(self, value):
        self.validate(value)
        self.__value = value

    @abstractmethod
    def validate(self, value):
        pass

    @property
    def value(self):
        return self.__value
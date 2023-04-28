# pylint: disable=missing-module-docstring
from abc import ABC, ABCMeta, abstractmethod
import json
from uc3m_logistics.order_management_exception import OrderManagementException
from uc3m_logistics.singleton_metaclass import SingletonMeta


# pylint: disable=missing-class-docstring
class FinalMeta(ABCMeta, SingletonMeta):
    pass


# pylint: disable=missing-class-docstring
class JsonStore(ABC, metaclass=FinalMeta):
    _FILE_PATH = None

    def __init__(self):
        self.__data = self.load()

    # pylint: disable=missing-function-docstring
    def load(self):
        try:
            with open(self._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError:
            # file not found
            data = []
            with open(self._FILE_PATH, "w", encoding="utf-8", newline="") as file:
                json.dump(data, file, indent=2)
        except json.decoder.JSONDecodeError:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format")
        return data

    def refresh(self):
        self.__data = self.load()

    def save(self):
        try:
            with open(self._FILE_PATH, "w", encoding="utf-8", newline="") as file:
                json.dump(self.__data, file, indent=2)

        except FileNotFoundError as ex:
            raise OrderManagementException("Wrong file or file path") from ex

    @abstractmethod
    def add_item(self):
        pass

    @abstractmethod
    def find_item_by_key(self, key):
        pass

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value
        self.save()

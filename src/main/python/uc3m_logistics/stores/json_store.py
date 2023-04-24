from abc import ABC, abstractmethod
import json
from ..order_management_exception import OrderManagementException

class JsonStore(ABC):
    _FILE_PATH = ""

    def __init__(self):
        self.__data = self.load()

    def load(self):
        try:
            with open(self._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            # file not found
            raise OrderManagementException("Store not found")



    def save(self):
        try:
            with open(self._FILE_PATH, "w+", encoding="utf-8", newline="") as file:
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
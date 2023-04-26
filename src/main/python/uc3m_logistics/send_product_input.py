import json

from .order_management_exception import OrderManagementException

from .validation.order_id_attribute import OrderIdAttribute
from .validation.email_attribute import EmailAttribute

class SendProductInput:

    def __init__(self, order_id, contact_email):
        self.__order_id = OrderIdAttribute(order_id).value
        self.__email = EmailAttribute(contact_email).value


    @property
    def order_id(self):
        return self.__order_id

    @order_id.setter
    def order_id(self, value):
        self.__order_id = OrderIdAttribute(value).value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = EmailAttribute(value).value

    @classmethod
    def from_json(cls, file_path):
        try:
            with open(file_path, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            # file is not found
            raise OrderManagementException("File is not found") from ex
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
        
        if "OrderID" not in data:
            raise OrderManagementException("Bad label")
        if "ContactEmail" not in data:
            raise OrderManagementException("Bad label")

        return cls(data["OrderID"], data["ContactEmail"])

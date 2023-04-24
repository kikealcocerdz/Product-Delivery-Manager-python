from .attribute import Attribute
import re

from uc3m_logistics.order_management_exception import OrderManagementException


class AddressAttribute(Attribute):

    def __init__(self, value:str):
        self.myregex = re.compile(r"^(?=^.{20,100}$)(([a-zA-Z0-9]+\s)+[a-zA-Z0-9]+)$")
        super().__init__(value)

    def validate(self, value):
        res = self.myregex.fullmatch(value)
        if not res:
            raise OrderManagementException("address is not valid")
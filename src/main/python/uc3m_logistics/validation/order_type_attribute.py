from .attribute import Attribute
import re

from uc3m_logistics.order_management_exception import OrderManagementException

class OrderTypeAttribute(Attribute):

    def __init__(self, value: str):
        self.myregex = re.compile(r"(Regular|Premium)")
        super().__init__(value)

    def validate(self, value):
        res = self.myregex.fullmatch(value)
        if not res:
            raise OrderManagementException("order_type is not valid")


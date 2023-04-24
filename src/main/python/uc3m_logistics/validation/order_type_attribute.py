from .attribute import Attribute
import re

from uc3m_logistics.order_management_exception import OrderManagementException

class OrderTypeAttribute(Attribute):

    myregex = re.compile(r"(Regular|Premium)")

    def validate(self, value):
        res = self.myregex.fullmatch(value)
        if not res:
            raise OrderManagementException("order_type is not valid")
    

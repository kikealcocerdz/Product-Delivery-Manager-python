import re

from uc3m_logistics.order_management_exception import OrderManagementException

from .attribute import Attribute

class OrderIdAttribute(Attribute):
    
    myregex = re.compile(r"[0-9a-fA-F]{32}$")

    def validate(self, value):
        res = self.myregex.fullmatch(value)
        if not res:
            raise OrderManagementException("order id is not valid")

    
# pylint: disable=missing-module-docstring
import re
from uc3m_logistics.order_management_exception import OrderManagementException
from uc3m_logistics.validation.attribute import Attribute


class OrderIdAttribute(Attribute):
    """OrderID validation"""
    myregex = re.compile(r"[0-9a-fA-F]{32}$")

    def validate(self, value):
        res = self.myregex.fullmatch(value)
        if not res:
            raise OrderManagementException("order id is not valid")

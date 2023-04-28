# pylint: disable=missing-module-docstring
import re
from uc3m_logistics.order_management_exception import OrderManagementException
from uc3m_logistics.validation.attribute import Attribute


class OrderTypeAttribute(Attribute):
    """order_type validation"""

    myregex = re.compile(r"(Regular|Premium)")

    def validate(self, value):
        res = self.myregex.fullmatch(value)
        if not res:
            raise OrderManagementException("order_type is not valid")

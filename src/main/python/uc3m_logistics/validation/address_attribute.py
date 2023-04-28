# pylint: disable=missing-module-docstring
import re
from uc3m_logistics.order_management_exception import OrderManagementException
from uc3m_logistics.validation.attribute import Attribute


class AddressAttribute(Attribute):
    """Address validation"""
    myregex = re.compile(r"^(?=^.{20,100}$)(([a-zA-Z0-9]+\s)+[a-zA-Z0-9]+)$")
    def validate(self, value):
        """Application of regex"""
        res = self.myregex.fullmatch(value)
        if not res:
            raise OrderManagementException("address is not valid")

# pylint: disable=missing-module-docstring
import re
from uc3m_logistics.order_management_exception import OrderManagementException
from uc3m_logistics.validation.attribute import Attribute


class EmailAttribute(Attribute):
    """Email validation"""
    regex_email = r'^[a-z0-9]+([\._]?[a-z0-9]+)+[@](\w+[.])+\w{2,3}$'
    myregex = re.compile(regex_email)

    def validate(self, value):
        res = self.myregex.fullmatch(value)
        if not res:
            raise OrderManagementException("contact email is not valid")

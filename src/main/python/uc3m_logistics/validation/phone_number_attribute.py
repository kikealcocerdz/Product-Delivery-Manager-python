# pylint: disable=missing-module-docstring
import re
from uc3m_logistics.order_management_exception import OrderManagementException
from uc3m_logistics.validation.attribute import Attribute


class PhoneNumberAttribute(Attribute):
    """phone_number validation"""

    myregex = re.compile(r"^(\+)[0-9]{11}")

    def validate(self, value):
        res = self.myregex.fullmatch(value)
        if not res:
            raise OrderManagementException("phone number is not valid")

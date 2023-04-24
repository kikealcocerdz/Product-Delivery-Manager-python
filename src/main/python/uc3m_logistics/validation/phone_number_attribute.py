from .attribute import Attribute
import re

from uc3m_logistics.order_management_exception import OrderManagementException


class PhoneNumberAttribute(Attribute):

    myregex = re.compile(r"^(\+)[0-9]{11}")

    def validate(self, value):
        res = self.myregex.fullmatch(value)
        if not res:
            raise OrderManagementException("phone number is not valid")

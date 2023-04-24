from .attribute import Attribute
import re

from uc3m_logistics.order_management_exception import OrderManagementException


class PhoneNumberAttribute(Attribute):

    def __init__(self, value:str):
        self.myregex = re.compile(r"^(\+)[0-9]{11}")
        super().__init__(value)

    def validate(self, value):
        res = self.myregex.fullmatch(value)
        if not res:
            raise OrderManagementException("phone number is not valid")

from .attribute import Attribute
import re

from uc3m_logistics.order_management_exception import OrderManagementException


class EmailAttribute(Attribute):

    regex_email = r'^[a-z0-9]+([\._]?[a-z0-9]+)+[@](\w+[.])+\w{2,3}$'
    myregex = re.compile(regex_email)
    
    def validate(self, value):
        res = self.myregex.fullmatch(value)
        if not res:
            raise OrderManagementException("contact email is not valid")

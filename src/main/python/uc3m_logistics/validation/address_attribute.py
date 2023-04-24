from .attribute import Attribute
import re

from uc3m_logistics.order_management_exception import OrderManagementException


class AddressAttribute(Attribute):
    
    myregex = re.compile(r"^(?=^.{20,100}$)(([a-zA-Z0-9]+\s)+[a-zA-Z0-9]+)$")

    def validate(self, value):
        res = self.myregex.fullmatch(value)
        if not res:
            raise OrderManagementException("address is not valid")
        
        
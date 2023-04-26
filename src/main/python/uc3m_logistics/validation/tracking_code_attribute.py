import re

from .attribute import Attribute
from ..order_management_exception import OrderManagementException

class TrackingCodeAttribute(Attribute):

    def validate(self, value):
        """Method for validating sha256 values"""
        myregex = re.compile(r"[0-9a-fA-F]{64}$")
        res = myregex.fullmatch(value)
        if not res:
            raise OrderManagementException("tracking_code format is not valid")

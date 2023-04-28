# pylint: disable=missing-module-docstring
import re
from uc3m_logistics.order_management_exception import OrderManagementException
from uc3m_logistics.validation.attribute import Attribute


class TrackingCodeAttribute(Attribute):
    """tracking_code validation"""

    def validate(self, value):
        """Method for validating sha256 values"""
        myregex = re.compile(r"[0-9a-fA-F]{64}$")
        res = myregex.fullmatch(value)
        if not res:
            raise OrderManagementException("tracking_code format is not valid")

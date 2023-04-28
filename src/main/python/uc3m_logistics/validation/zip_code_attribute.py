# pylint: disable=missing-module-docstring
from uc3m_logistics.order_management_exception import OrderManagementException
from uc3m_logistics.validation.attribute import Attribute


class ZipCodeAttribute(Attribute):
    """zip_code validation"""

    def validate(self, value):
        if value.isnumeric() and len(value) == 5:
            if int(value) > 52999 or int(value) < 1000:
                raise OrderManagementException("zip_code is not valid")
        else:
            raise OrderManagementException("zip_code format is not valid")

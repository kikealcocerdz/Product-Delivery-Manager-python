from .attribute import Attribute
from uc3m_logistics.order_management_exception import OrderManagementException


class ZipCodeAttribute(Attribute):

    def validate(self, value):
        if value.isnumeric() and len(value) == 5:
            if (int(value) > 52999 or int(value) < 1000):
                raise OrderManagementException("zip_code is not valid")
        else:
            raise OrderManagementException("zip_code format is not valid")

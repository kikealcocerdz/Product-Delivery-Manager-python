"""Definition of attribute ProductId"""
from uc3m_logistics.attributes.attribute import Attribute
from uc3m_logistics.exception.order_management_exception import OrderManagementException


class ProductId(Attribute):
    """Definition of attribute ProductId class"""

    # pylint: disable=super-init-not-called, too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute ProductId init"""
        self._validation_pattern = r"^[0-9]{13}$"
        self._error_message  = "Invalid EAN13 code string"
        self._attr_value = self._validate(attr_value)

    def _validate( self, attr_value ):
        """method vor validating a ean13 code"""
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE EAN13
        # RETURN TRUE IF THE EAN13 IS RIGHT, OR FALSE IN OTHER CASE
        checksum = 0
        code_read = -1
        super()._validate(attr_value)

        for i, digit in enumerate(reversed(attr_value)):
            try:
                current_digit = int(digit)
            except ValueError as v_e:
                raise OrderManagementException("Invalid EAN13 code string") from v_e
            if i == 0:
                code_read = current_digit
            else:
                checksum += (current_digit) * 3 if (i % 2 != 0) else current_digit
        control_digit = (10 - (checksum % 10)) % 10

        if (code_read != -1) and (code_read == control_digit):
            res = attr_value
        else:
            raise OrderManagementException("Invalid EAN13 control digit")
        return res

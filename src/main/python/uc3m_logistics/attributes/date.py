from uc3m_logistics.attributes.attribute import Attribute

class Date(Attribute):

    def __init__(self, attr_value):
        self._validation_pattern = r"^(0[1-9]|1[0-2])-(0[1-9]|1\d|2\d|3[01])-(\d{4})$"
        self._error_message = "Date must follow the format: MM-DD-YYYY"
        self._attr_value = self._validate(attr_value)
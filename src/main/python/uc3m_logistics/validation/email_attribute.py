
from .attribute import Attribute

class EmailAttribute(Attribute):

    def __init__(self, value: str):
        super().__init__(value)

    def validate(self, value):


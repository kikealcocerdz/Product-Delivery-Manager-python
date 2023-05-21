import json
from uc3m_logistics.inputs.input_file import InputFile
from uc3m_logistics.exception.order_management_exception import OrderManagementException
from uc3m_logistics.attributes.date import Date
from uc3m_logistics.attributes.tracking_code import TrackingCode

class ModifyDeliveryInputFile(InputFile):

    def __init__(self, input_file):
        data = self.get_data_from_input_file(input_file)
        self.tracking_code = TrackingCode(data['tracking_code']).value
        self.date = Date(data['date']).value

    def get_data_from_input_file(self, input_file):
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            raise OrderManagementException("File not found") from ex
        except json.JSONDecodeError as ex:
            raise OrderManagementException("Invalid JSON format") from ex

        self.validate_input_file_labels(data)

        return data

    def validate_input_file_labels(self, data):
        if 'tracking_code' not in data.keys():
            raise OrderManagementException("Invalid JSON format")
        elif 'date' not in data.keys():
            raise OrderManagementException("Invalid JSON format")

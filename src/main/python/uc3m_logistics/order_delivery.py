# pylint: disable=missing-module-docstring
import json
from datetime import datetime
from uc3m_logistics.order_management_exception import OrderManagementException
from uc3m_logistics.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.stores.order_delivery_store import OrderDeliveryStore
from uc3m_logistics.validation.tracking_code_attribute import TrackingCodeAttribute


class OrderDelivery:
    """Class to check if the order is correct"""

    def __init__(self, tracking_code):
        self.__tracking_code = TrackingCodeAttribute(tracking_code).value
        self.__delivery_date = str(datetime.utcnow())

    # pylint: disable=missing-function-docstring
    def save_to_store(self):
        OrderDeliveryStore().add_item(self)

    # pylint: disable=missing-function-docstring
    @property
    def tracking_code(self):
        return self.__tracking_code

    @tracking_code.setter
    def tracking_code(self, value):
        self.__tracking_code = TrackingCodeAttribute(value).value

    @property
    def delivery_date(self):
        return self.__delivery_date

    @delivery_date.setter
    def delivery_date(self, value):
        self.__delivery_date = value

    @staticmethod
    def from_order_tracking_code(tracking_code):
        tracking_code = TrackingCodeAttribute(tracking_code).value

        # check if this tracking_code is in shipments_store
        shipments_store_file = JSON_FILES_PATH + "shipments_store.json"
        # first read the file
        try:
            with open(shipments_store_file, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
        except FileNotFoundError as ex:
            raise OrderManagementException("shipments_store not found") from ex
        # search this tracking_code
        found = False
        for item in data_list:
            if item["_OrderShipping__tracking_code"] == tracking_code:
                found = True
                delivery_day = item["_OrderShipping__delivery_day"]

        if not found:
            raise OrderManagementException("tracking_code is not found")

        today = datetime.today().date()
        delivery_date = datetime.fromtimestamp(delivery_day).date()
        if delivery_date != today:
            raise OrderManagementException("Today is not the delivery date")
        return OrderDelivery(tracking_code)

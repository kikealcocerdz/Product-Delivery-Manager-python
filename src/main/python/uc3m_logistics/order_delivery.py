# pylint: disable=missing-module-docstring
from datetime import datetime
from uc3m_logistics.order_management_exception import OrderManagementException
from uc3m_logistics.stores.order_delivery_store import OrderDeliveryStore
from uc3m_logistics.validation.tracking_code_attribute import TrackingCodeAttribute
from uc3m_logistics.stores.order_shipping_store import OrderShippingStore


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

        shipping = OrderShippingStore().find_item_by_key(tracking_code)
        delivery_day = shipping.delivery_day

        today = datetime.today().date()
        delivery_date = datetime.fromtimestamp(delivery_day).date()
        if delivery_date != today:
            raise OrderManagementException("Today is not the delivery date")
        return OrderDelivery(tracking_code)

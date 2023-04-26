
from datetime import datetime
from uc3m_logistics import OrderDeliveryStore
from .validation.tracking_code_attribute import TrackingCodeAttribute
from uc3m_logistics.order_management_exception import OrderManagementException

class OrderDelivery:

    def __init__(self, tracking_code):
        self.__tracking_code = TrackingCodeAttribute(tracking_code).value
        self.__delivery_date = str(datetime.utcnow())

    def save_to_store(self):
        pass

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

    @classmethod
    def from_order_tracking_code(cls, tracking_code):
        return OrderDeliveryStore().find_item_by_key(tracking_code)

    def save_to_store(self):
        OrderDeliveryStore().add_item(self)
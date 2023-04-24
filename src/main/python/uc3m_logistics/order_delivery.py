

class OrderDelivery:

    def __init__(self, tracking_code):
        pass

    def save_to_store(self):
        pass

    @property
    def tracking_code(self):
        return self.__tracking_code

    @tracking_code.setter
    def tracking_code(self, value):
        self.__tracking_code = TrackingCodeAttribute(value).value

    @classmethod
    def from_order_tracking_code(cls, tracking_code):
        return OrderDeliveryStore().find_item_by_key(tracking_code)

    def save_to_store(self):
        OrderDeliveryStore().add_item(self)
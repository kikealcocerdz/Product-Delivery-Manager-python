# pylint: disable=missing-module-docstring
from datetime import datetime
from freezegun import freeze_time
from uc3m_logistics.stores.json_store import JsonStore
from uc3m_logistics.order_manager_config import JSON_FILES_PATH


class OrderDeliveryStore(JsonStore):
    """Store for OrderDelivery"""
    _FILE_PATH = JSON_FILES_PATH + "shipments_delivered.json"

    def add_item(self, item):
        self.refresh()
        self.data.append(item.tracking_code)
        self.data.append(item.delivery_date)
        self.save()

    def find_item_by_key(self, key):
        for index, elem in enumerate(self.data):
            if elem == key:
                tracking_code = elem
                delivery_date = self.data[index + 1]
                with freeze_time(datetime.fromtimestamp(delivery_date).date()):
                    # pylint: disable=import-outside-toplevel
                    from uc3m_logistics.order_delivery import OrderDelivery
                    return OrderDelivery(tracking_code)

        return None

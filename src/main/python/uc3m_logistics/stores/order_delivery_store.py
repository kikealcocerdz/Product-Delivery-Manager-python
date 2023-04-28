# pylint: disable=missing-module-docstring
from uc3m_logistics.stores.json_store import JsonStore
from uc3m_logistics.order_manager_config import JSON_FILES_PATH


class OrderDeliveryStore(JsonStore):
    """Store for OrderDelivery"""
    _FILE_PATH = JSON_FILES_PATH + "shipments_delivered.json"

    def add_item(self, new_item):
        self.refresh()
        self.data.append(new_item.tracking_code)
        self.data.append(new_item.delivery_date)
        self.save()

    def find_item_by_key(self, key):
        pass

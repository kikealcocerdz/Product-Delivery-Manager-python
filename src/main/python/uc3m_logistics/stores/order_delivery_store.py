from .json_store import JsonStore
from ..order_manager_config import JSON_FILES_PATH
from freezegun import freeze_time
from datetime import datetime
from ..order_management_exception import OrderManagementException

class OrderDeliveryStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "shipments_delivered.json"

    def add_item(self, new_item):
        self.refresh()
        
        self.data.append(new_item.tracking_code)
        self.data.append(new_item.delivery_date)
        
        self.save()

    def find_item_by_key(self, key):
        pass
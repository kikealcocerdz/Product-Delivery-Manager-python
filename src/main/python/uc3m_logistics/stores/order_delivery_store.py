from .json_store import JsonStore

from ..order_management_exception import OrderManagementException
from uc3m_logistics.order_manager_config import JSON_FILES_PATH

class OrderDeliveryStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "shipments_delivered.json"



    def add_item(self, new_item):
        found = False
        for item in self.data:
            if item["_OrderRequest__order_id"] == new_item.order_id:
                found = True
        if not found:
            self.data.append(new_item.__dict__)
        else:
            raise OrderManagementException("order_id is already registered in orders_store")

        self.save()
from .json_store import JsonStore

from ..order_management_exception import OrderManagementException
from .. import JSON_FILES_PATH

class OrderRequestStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "orders_store.json"



    def add_item(self, new_item):
        found = False
        for item in self.data:
            if item["_OrderRequest__order_id"] == new_item.order_id:
                found = True
        if not found:
            self.data.append(new_item.__dict__)
        else:
            raise OrderManagementException("Could not find order in order_requests store")

        self.save()
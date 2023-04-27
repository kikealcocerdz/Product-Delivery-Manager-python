from ..order_manager_config import JSON_FILES_PATH
from .json_store import JsonStore

class OrderShippingStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "shipments_store.json"


    def find_item_by_key(self, key: str):
        # refresh the store
        self.refresh()

        for item in self.data:
            if item["_OrderShipping__tracking_code"]:
                return item

        return None

    def add_item(self, new_shipping):
        self.refresh()
        self.data.append(new_shipping.__dict__)
        self.save()
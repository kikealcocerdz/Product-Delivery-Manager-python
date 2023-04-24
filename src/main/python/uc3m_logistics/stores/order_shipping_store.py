
from .json_store import JsonStore

class OrderShippingStore(JsonStore):

    def find_item_by_key(self, key: str):
        for item in self.data:
            if item["_OrderShipping__tracking_code"]:
                return item

        return None

    def add_item(self, new_item):
        self.data.append(new_item.__dict__)
        self.save()
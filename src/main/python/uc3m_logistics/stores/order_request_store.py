from freezegun import freeze_time
from datetime import datetime

from .json_store import JsonStore

from ..order_management_exception import OrderManagementException

from uc3m_logistics.order_manager_config import JSON_FILES_PATH

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
            raise OrderManagementException("order_id is already registered in orders_store")

        self.save()

    def find_item_by_key(self, key: str):
        found_item: dict or None = None

        for item in self.data:
            if item["_OrderRequest__order_id"] == key:
                found_item = item
                break

        if found_item:
            product_id = found_item["_OrderRequest__product_id"]
            address = found_item["_OrderRequest__delivery_address"]
            order_type = found_item["_OrderRequest__order_type"]
            phone_number = found_item["_OrderRequest__phone_number"]
            zip_code = found_item["_OrderRequest__zip_code"]
            order_timestamp = found_item["_OrderRequest__time_stamp"]

            with freeze_time(datetime.fromtimestamp(order_timestamp).date()):
                from uc3m_logistics.order_request import OrderRequest
                order = OrderRequest(
                    product_id, order_type,
                    address, phone_number, zip_code 
                )
            
            if order.order_id != found_item["_OrderRequest__order_id"]:
                raise OrderManagementException("Orders' data have been manipulated")

            return order
        else:
            raise OrderManagementException("Order_id not found in order_requests store")
            
        return None
# pylint: disable=missing-module-docstring
from datetime import datetime
from freezegun import freeze_time
from uc3m_logistics.stores.json_store import JsonStore
from uc3m_logistics.order_management_exception import OrderManagementException
from uc3m_logistics.order_manager_config import JSON_FILES_PATH


class OrderRequestStore(JsonStore):
    """Store for OrderRequest"""
    _FILE_PATH = JSON_FILES_PATH + "orders_store.json"

    def add_item(self, item):
        self.refresh()
        found = False
        for found_item in self.data:
            if found_item["_OrderRequest__order_id"] == item.order_id:
                found = True
        if found is False:
            self.data.append(item.__dict__)
        else:
            raise OrderManagementException("order_id is already registered in orders_store")

        self.save()

    def find_item_by_key(self, key: str):
        # refresh the store before taking an action
        self.refresh()
        found_item = None

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
                # lazy import OrderRequest to avoid circular import
                # pylint: disable=import-outside-toplevel
                from uc3m_logistics.order_request import OrderRequest
                order = OrderRequest(
                    product_id, order_type,
                    address, phone_number, zip_code)
            if order.order_id != found_item["_OrderRequest__order_id"]:
                raise OrderManagementException("Orders' data have been manipulated")

            return order
        # if order not found
        raise OrderManagementException("Order_id not found in order_requests store")

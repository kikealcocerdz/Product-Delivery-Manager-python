# pylint: disable=missing-module-docstring
from datetime import datetime
from freezegun import freeze_time
from uc3m_logistics.order_manager_config import JSON_FILES_PATH
from uc3m_logistics.stores.json_store import JsonStore
from uc3m_logistics.stores.order_request_store import OrderRequestStore
from uc3m_logistics.order_management_exception import OrderManagementException

class OrderShippingStore(JsonStore):
    """Store for OrderShipping"""
    _FILE_PATH = JSON_FILES_PATH + "shipments_store.json"

    def find_item_by_key(self, key: str):
        # refresh the store
        self.refresh()

        found_item = None

        for item in self.data:
            if item["_OrderShipping__tracking_code"] == key:
                found_item = item
                break

        if found_item:
            product_id = found_item["_OrderShipping__product_id"]
            order_id = found_item["_OrderShipping__order_id"]
            delivery_email = found_item["_OrderShipping__delivery_email"]
            issued_at = found_item["_OrderShipping__issued_at"]
            order_type = OrderRequestStore().find_item_by_key(order_id).order_type

            with freeze_time(datetime.fromtimestamp(issued_at).date()):
                # lazy import OrderShipping to avoid circular import
                # pylint: disable=import-outside-toplevel
                from uc3m_logistics.order_shipping import OrderShipping
                return OrderShipping(product_id, order_id, delivery_email, order_type)

        raise OrderManagementException("tracking_code is not found")

    def add_item(self, item):
        self.refresh()
        self.data.append(item.__dict__)
        self.save()

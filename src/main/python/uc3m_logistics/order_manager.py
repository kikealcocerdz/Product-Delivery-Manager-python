"""Module """
import datetime
import re
import json
from datetime import datetime
from freezegun import freeze_time
from .order_request import OrderRequest
from .order_management_exception import OrderManagementException
from .order_shipping import OrderShipping
from .order_delivery import OrderDelivery
from .validation.tracking_code_attribute import TrackingCodeAttribute
from .order_manager_config import JSON_FILES_PATH
from .singleton_metaclass import SingletonMeta

class OrderManager(metaclass=SingletonMeta):
    """Class for providing the methods for managing the orders process"""

    # pylint: disable=too-many-arguments
    def register_order(self, product_id,
                       order_type,
                       address,
                       phone_number,
                       zip_code):
        """Register the orders into the order's file"""

        order_request = OrderRequest(product_id, order_type, address, phone_number, zip_code)

        order_request.save_to_store()

        return order_request.order_id

    # pylint: disable=too-many-locals
    def send_product(self, input_file):
        """Sends the order included in the input_file"""
        my_sign = OrderShipping.from_send_input_file(input_file)

        my_sign.save_to_store()

        return my_sign.tracking_code

    def deliver_product(self, tracking_code):
        """Register the delivery of the product"""
        delivery = OrderDelivery.from_order_tracking_code(tracking_code)

        delivery.save_to_store()
        return True
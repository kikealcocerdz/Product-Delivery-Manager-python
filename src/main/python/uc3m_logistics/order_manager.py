"""Module """
from uc3m_logistics.order_request import OrderRequest
from uc3m_logistics.singleton_metaclass import SingletonMeta
from uc3m_logistics.order_shipping import OrderShipping
from uc3m_logistics.order_delivery import OrderDelivery


class OrderManager(metaclass=SingletonMeta):
    """Class for providing the methods for managing the orders process"""

    # pylint: disable=too-many-arguments
    @staticmethod
    def register_order(product_id,
                       order_type,
                       address,
                       phone_number,
                       zip_code):
        """Register the orders into the order's file"""

        order_request = OrderRequest(product_id, order_type, address, phone_number, zip_code)

        order_request.save_to_store()

        return order_request.order_id

    # pylint: disable=too-many-locals
    @staticmethod
    def send_product(input_file):
        """Sends the order included in the input_file"""
        my_sign = OrderShipping.from_send_input_file(input_file)

        my_sign.save_to_store()

        return my_sign.tracking_code

    @staticmethod
    def deliver_product(tracking_code):
        """Register the delivery of the product"""
        delivery = OrderDelivery.from_order_tracking_code(tracking_code)

        delivery.save_to_store()
        return True

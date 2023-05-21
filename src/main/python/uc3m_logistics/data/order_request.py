"""MODULE: order_request. Contains the order request class"""
import hashlib
import json
from datetime import datetime
from uc3m_logistics.exception.order_management_exception import OrderManagementException
from uc3m_logistics.attributes.order_type import OrderType
from uc3m_logistics.attributes.product_id import ProductId
from uc3m_logistics.attributes.address import Address
from uc3m_logistics.attributes.phone_number import PhoneNumber
from uc3m_logistics.attributes.zip_code import ZipCode
from uc3m_logistics.storage.orders_json_store import OrdersJsonStore
from freezegun import freeze_time

class OrderRequest:
    """Class representing the register of the order in the system"""
    #pylint: disable=too-many-arguments
    def __init__( self, product_id, order_type,
                  delivery_address, phone_number, zip_code ):
        self.__product_id = ProductId(product_id).value
        self.__delivery_address = Address(delivery_address).value
        self.__order_type = OrderType(order_type).value
        self.__phone_number = PhoneNumber(phone_number).value
        self.__zip_code = ZipCode(zip_code).value
        justnow = datetime.utcnow()
        self.__time_stamp = datetime.timestamp(justnow)
        self.__order_id =  hashlib.md5(self.__str__().encode()).hexdigest()

    @classmethod
    def get_order_by_order_id( cls, order_id ):
        """creates the order from the file"""
        orders_store = OrdersJsonStore()
        item = orders_store.find_item(order_id, "_OrderRequest__order_id")
        if not item:
            raise OrderManagementException("order_id not found")
        # retrieve the orders data
        proid = item["_OrderRequest__product_id"]
        address = item["_OrderRequest__delivery_address"]
        reg_type = item["_OrderRequest__order_type"]
        phone = item["_OrderRequest__phone_number"]
        order_timestamp = item["_OrderRequest__time_stamp"]
        zip_code = item["_OrderRequest__zip_code"]
        # set the time when the order was registered for checking the md5
        with freeze_time(datetime.fromtimestamp(order_timestamp).date()):
            order = cls(product_id=proid,
                                 delivery_address=address,
                                 order_type=reg_type,
                                 phone_number=phone,
                                 zip_code=zip_code)
        if order.order_id != order_id:
            raise OrderManagementException("Orders' data have been manipulated")
        return order

    def save( self ):
        """saves the order into the store"""
        orders_store = OrdersJsonStore()
        orders_store.add_item(self)

    def __str__(self):
        return "OrderRequest:" + json.dumps(self.__dict__)


    @property
    def delivery_address( self ):
        """Property representing the address where the product
        must be delivered"""
        return self.__delivery_address

    @delivery_address.setter
    def delivery_address( self, value ):
        self.__delivery_address = value

    @property
    def order_type( self ):
        """Property representing the type of order: REGULAR or PREMIUM"""
        return self.__order_type
    @order_type.setter
    def order_type( self, value ):
        self.__order_type = value

    @property
    def phone_number( self ):
        """Property representing the clients's phone number"""
        return self.__phone_number
    @phone_number.setter
    def phone_number( self, value ):
        self.__phone_number = value

    @property
    def product_id( self ):
        """Property representing the products  EAN13 code"""
        return self.__product_id
    @product_id.setter
    def product_id( self, value ):
        self.__product_id = value

    @property
    def time_stamp(self):
        """Read-only property that returns the timestamp of the request"""
        return self.__time_stamp

    @property
    def order_id( self ):
        """Returns the md5 signature"""
        return self.__order_id

    @property
    def zip_code( self ):
        """Returns the order's zip_code"""
        return self.__zip_code

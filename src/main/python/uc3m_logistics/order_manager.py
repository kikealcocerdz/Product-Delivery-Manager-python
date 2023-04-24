"""Module """
import datetime
import re
import json
from datetime import datetime
from freezegun import freeze_time
from .order_request import OrderRequest
from .order_management_exception import OrderManagementException
from .order_shipping import OrderShipping
from .order_manager_config import JSON_FILES_PATH
from .send_product_input import SendProductInput
from .stores.order_request_store import OrderRequestStore
from .validation.product_id_attribute import ProductIdAttribute
from .validation.order_type_attribute import OrderTypeAttribute
from .validation.address_attribute import AddressAttribute
from .validation.phone_number_attribute import PhoneNumberAttribute
from .validation.zip_code_attribute import ZipCodeAttribute
from .validation.email_attribute import EmailAttribute


class OrderManager:
    """Class for providing the methods for managing the orders process"""

    def __init__(self):
        pass

    @staticmethod
    def validate_tracking_code(t_c):
        """Method for validating sha256 values"""
        myregex = re.compile(r"[0-9a-fA-F]{64}$")
        res = myregex.fullmatch(t_c)
        if not res:
            raise OrderManagementException("tracking_code format is not valid")

    @staticmethod
    def save_store(data):
        """Medthod for saving the orders store"""
        file_store = JSON_FILES_PATH + "orders_store.json"
        # first read the file
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            data_list = []
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex

        found = False
        for item in data_list:
            if item["_OrderRequest__order_id"] == data.order_id:
                found = True
        if found is False:
            data_list.append(data.__dict__)
        else:
            raise OrderManagementException("order_id is already registered in orders_store")
        try:
            with open(file_store, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise OrderManagementException("Wrong file or file path") from ex
        return True

    @staticmethod
    def save_fast(data):
        """Method for saving the orders store"""
        orders_store = JSON_FILES_PATH + "orders_store.json"
        with open(orders_store, "r+", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
            data_list.append(data.__dict__)
            file.seek(0)
            json.dump(data_list, file, indent=2)

    @staticmethod
    def save_orders_shipped(shipment):
        """Saves the shipping object into a file"""
        shipments_store_file = JSON_FILES_PATH + "shipments_store.json"
        # first read the file
        try:
            with open(shipments_store_file, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            data_list = []
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex

        # append the shipments list
        data_list.append(shipment.__dict__)

        try:
            with open(shipments_store_file, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise OrderManagementException("Wrong file or file path") from ex

    # pylint: disable=too-many-arguments
    def register_order(self, product_id: str,
                       order_type: str,
                       address: str,
                       phone_number: str,
                       zip_code: str) -> str:
        """Register the orders into the order's file"""
        
        my_order = OrderRequest(ProductIdAttribute(product_id).value,
                                OrderTypeAttribute(order_type).value,
                                AddressAttribute(address).value,
                                PhoneNumberAttribute(phone_number).value,
                                ZipCodeAttribute(zip_code).value)
                                
        self.save_store(my_order)

        return my_order.order_id

    # pylint: disable=too-many-locals
    def send_product(self, input_file):
        """Sends the order included in the input_file"""
        send_product_input = SendProductInput.from_json(input_file)

        order_request = OrderRequestStore().find_item_by_key(send_product_input.order_id)

        order_shipping = OrderShipping(product_id=order_request.product_id,
                                       order_id=send_product_input.order_id,
                                       order_type=order_request.order_type,
                                       delivery_email=send_product_input.email)

        # check all the information
        try:
            myregex = re.compile(r"[0-9a-fA-F]{32}$")
            res = myregex.fullmatch(data["OrderID"])
            if not res:
                raise OrderManagementException("order id is not valid")
        except KeyError as ex:
            raise OrderManagementException("Bad label") from ex

        try:
            regex_email = r'^[a-z0-9]+([\._]?[a-z0-9]+)+[@](\w+[.])+\w{2,3}$'
            myregex = re.compile(regex_email)
            res = myregex.fullmatch(data["ContactEmail"])
            if not res:
                raise OrderManagementException("contact email is not valid")
        except KeyError as ex:
            raise OrderManagementException("Bad label") from ex
        file_store = JSON_FILES_PATH + "orders_store.json"

        with open(file_store, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
        found = False
        for item in data_list:
            if item["_OrderRequest__order_id"] == data["OrderID"]:
                found = True
                # retrieve the orders data
                product_id = item["_OrderRequest__product_id"]
                address = item["_OrderRequest__delivery_address"]
                order_type = item["_OrderRequest__order_type"]
                phone_number = item["_OrderRequest__phone_number"]
                order_timestamp = item["_OrderRequest__time_stamp"]
                zip_code = item["_OrderRequest__zip_code"]
                # set the time when the order was registered for checking the md5
                with freeze_time(datetime.fromtimestamp(order_timestamp).date()):
                    order = OrderRequest(product_id=product_id,
                                         delivery_address=address,
                                         order_type=order_type,
                                         phone_number=phone_number,
                                         zip_code=zip_code)

                if order.order_id != data["OrderID"]:
                    raise OrderManagementException("Orders' data have been manipulated")

        if not found:
            raise OrderManagementException("order_id not found")

        my_sign = OrderShipping(product_id=product_id,
                                order_id=data["OrderID"],
                                order_type=order_type,
                                delivery_email=data["ContactEmail"])

        # save the OrderShipping in shipments_store.json

        self.save_orders_shipped(my_sign)

        return my_sign.tracking_code

    def deliver_product(self, tracking_code):
        """Register the delivery of the product"""
        order_shipping = OrderShipping.from_tracking_code(tracking_code)

        self.validate_tracking_code(tracking_code)

        # check if this tracking_code is in shipments_store
        shipments_store_file = JSON_FILES_PATH + "shipments_store.json"
        # first read the file
        try:
            with open(shipments_store_file, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex
        except FileNotFoundError as ex:
            raise OrderManagementException("shipments_store not found") from ex
        # search this tracking_code
        found = False
        for item in data_list:
            if item["_OrderShipping__tracking_code"] == tracking_code:
                found = True
                delivery_day = item["_OrderShipping__delivery_day"]
        if not found:
            raise OrderManagementException("tracking_code is not found")

        today = datetime.today().date()
        delivery_date = datetime.fromtimestamp(delivery_day).date()
        if delivery_date != today:
            raise OrderManagementException("Today is not the delivery date")

        shipments_file = JSON_FILES_PATH + "shipments_delivered.json"

        try:
            with open(shipments_file, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError as ex:
            # file is not found , so  init my data_list
            data_list = []
        except json.JSONDecodeError as ex:
            raise OrderManagementException("JSON Decode Error - Wrong JSON Format") from ex

        # append the delivery info
        data_list.append(str(tracking_code))
        data_list.append(str(datetime.utcnow()))
        try:
            with open(shipments_file, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise OrderManagementException("Wrong file or file path") from ex
        return True

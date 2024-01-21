from dataclasses import dataclass
from typing import Any

from hasta_la_vista_money.receipts.models import Customer, Product, Receipt
from hasta_la_vista_money.users.models import User


@dataclass
class ProductData:
    user: User
    product_name: str
    price: float
    quantity: int
    amount: float
    nds_type: int
    nds_sum: float


@dataclass
class CustomerData:
    user: User
    name_seller: str
    retail_place_address: str
    retail_place: str


@dataclass
class ReceiptData:
    user: User
    account: Any
    receipt_date: str
    number_receipt: int
    nds10: int
    nds20: int
    operation_type: int
    total_sum: float
    customer: str


class ReceiptDataWriter:
    @classmethod
    def create_product(cls, product_data: ProductData):
        return Product.objects.create(
            user=product_data.user,
            product_name=product_data.product_name,
            price=product_data.price,
            quantity=product_data.quantity,
            amount=product_data.amount,
            nds_type=product_data.nds_type,
            nds_sum=product_data.nds_sum,
        )

    @classmethod
    def create_customer(cls, customer_data: CustomerData):
        return Customer.objects.create(
            user=customer_data.user,
            name_seller=customer_data.name_seller,
            retail_place_address=customer_data.retail_place_address,
            retail_place=customer_data.retail_place,
        )

    @classmethod
    def create_receipt(cls, receipt_data: ReceiptData):
        return Receipt.objects.create(
            user=receipt_data.user,
            account=receipt_data.account,
            receipt_date=receipt_data.receipt_date,
            number_receipt=receipt_data.number_receipt,
            nds10=receipt_data.nds10,
            nds20=receipt_data.nds20,
            operation_type=receipt_data.operation_type,
            total_sum=receipt_data.total_sum,
            customer=receipt_data.customer,
        )

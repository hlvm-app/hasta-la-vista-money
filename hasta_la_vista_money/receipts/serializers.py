from hasta_la_vista_money.receipts.models import Customer, Product, Receipt
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('created_at',)


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ('created_at',)


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        exclude = ('created_at',)

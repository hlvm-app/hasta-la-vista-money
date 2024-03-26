from rest_framework import serializers

from hasta_la_vista_money.receipts.models import Product, Customer, Receipt


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

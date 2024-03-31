from hasta_la_vista_money.receipts.models import Customer, Product, Receipt
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReceiptSerializer(ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = Receipt
        fields = '__all__'

    def create(self, validated_data):
        products_data = validated_data.pop('product')
        customer_data = validated_data.pop('customer')
        customer_serializer = CustomerSerializer(data=customer_data)
        if not customer_serializer.is_valid():
            raise ValidationError('Invalid customer data')
        customer = customer_serializer.save()
        receipt = Receipt.objects.create(customer=customer, **validated_data)
        for product_data in products_data:
            product_serializer = ProductSerializer(data=product_data)
            if not product_serializer.is_valid():
                raise ValidationError('Invalid product data')
            product = product_serializer.save()
            receipt.product.add(product)
        return receipt

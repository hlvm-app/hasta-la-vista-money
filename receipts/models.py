from django.db import models


class Customers(models.Model):
    name_seller = models.CharField(max_length=255)
    retail_place_address = models.CharField(max_length=256, null=True)
    retail_place = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name_seller


class CashReceipts(models.Model):
    receipt_date = models.DateTimeField()
    operation_type = models.IntegerField(null=True, blank=True)
    total_sum = models.DecimalField(max_digits=20, decimal_places=2)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='cashreceipts')

    def __str__(self):
        return self.receipt_date


class GoodsInReceipt(models.Model):
    receipt = models.ForeignKey(CashReceipts, on_delete=models.CASCADE, related_name='goodsinreceipt')
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='goodsinreceipts')

    def __str__(self):
        return self.product_name

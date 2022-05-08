from django.db import models


class Receipts(models.Model):
    receipt_date = models.CharField(max_length=20)
    name_seller = models.CharField(max_length=150)
    product_information = models.CharField(max_length=1000)
    total_sum = models.CharField(max_length=20)
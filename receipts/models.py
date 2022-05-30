from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone


class Receipt(models.Model):
    receipt_date = models.DateTimeField()
    name_seller = models.CharField(max_length=150)
    product_information = ArrayField(ArrayField(
            models.CharField(max_length=1000), default=list
        )
    )
    total_sum = models.CharField(max_length=20)

    def __str__(self):
        return self.name_seller

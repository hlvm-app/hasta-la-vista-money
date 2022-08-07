from django.db import models
from django.contrib.postgres.fields import ArrayField


class Receipt(models.Model):
    receipt_date = models.DateTimeField()
    name_seller = models.CharField(max_length=150)
    retail_place_address = models.CharField(max_length=256, null=True)
    operation_type = models.IntegerField(null=True, blank=True)
    retail_place = models.CharField(null=True, blank=True, max_length=256)
    product_information = ArrayField(ArrayField(
            models.CharField(max_length=1000), default=list
        )
    )
    total_sum = models.CharField(max_length=20)

    def __str__(self):
        return self.name_seller

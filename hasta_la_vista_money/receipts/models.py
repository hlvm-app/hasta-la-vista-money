from django.db import models
from django.utils.translation import gettext_lazy as _

OPERATION_TYPES = (
    (1, _('Приход')),
    (2, _('Возврат прихода')),
    (3, _('Расход')),
    (4, _('Возврат расхода')),
)


class Customer(models.Model):
    """Модель продавца."""

    name_seller = models.CharField(max_length=255)  # noqa: WPS432
    retail_place_address = models.CharField(
        default='Нет данных',
        null=True,
        max_length=1000,
    )
    retail_place = models.CharField(
        default='Нет данных',
        null=True,
        blank=True,
        max_length=1000,
    )

    def __str__(self):
        return self.name_seller


class Receipt(models.Model):
    """Модель чека."""

    receipt_date = models.DateTimeField()
    number_receipt = models.IntegerField(default=None, null=True)
    operation_type = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        choices=OPERATION_TYPES,
    )
    total_sum = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name='customer',
        related_name='customer',
    )
    product = models.ManyToManyField('Product', related_name='product')

    def datetime(self):
        return self.receipt_date


class Product(models.Model):
    """Модель продуктов."""

    product_name = models.CharField(default='Нет данных', max_length=1000)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    quantity = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    nds_type = models.IntegerField(default=None, null=True, blank=True)
    nds_sum = models.DecimalField(
        default=0,
        null=True,
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return self.product_name

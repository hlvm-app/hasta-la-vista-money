import django_filters
from django_filters import rest_framework as filters
from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext

from receipts.models import Receipt


class ReceiptForm(ModelForm):
    class Meta:
        model = Receipt
        fields = ('name_seller',)
        labels = {
            'name_seller': gettext('Продавец')
        }


class ReceiptsFilter(filters.FilterSet):
    names_seller = Receipt.objects.values_list('id', 'name_seller', named=True).all()
    name_seller = filters.ChoiceFilter(label='Seller', choices=names_seller)

    class Meta:
        model = Receipt
        fields = ('name_seller', )

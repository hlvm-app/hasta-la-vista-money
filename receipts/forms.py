import django_filters
from django_filters import rest_framework as filters
from django.utils.translation import gettext_lazy

from receipts.models import Receipt


class ReceiptsFilter(django_filters.FilterSet):
    names_seller = Receipt.objects.values_list('name_seller', 'name_seller').distinct()
    name_seller = filters.ChoiceFilter(label='Seller', choices=names_seller)

    class Meta:
        model = Receipt
        fields = ('name_seller', )

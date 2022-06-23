import django_filters
from django.forms import ModelForm
from django.utils.translation import gettext_lazy

from receipts.models import Receipt


class ReceiptsFilter(django_filters.FilterSet):
    names_seller = Receipt.objects.values_list('name_seller',
                                               'name_seller').distinct()
    name_seller = django_filters.ChoiceFilter(label=gettext_lazy('Продавец'),
                                              choices=names_seller)
    receipt_date = django_filters.DateRangeFilter(label=gettext_lazy('Период'))

    class Meta:
        model = Receipt
        fields = ('name_seller', 'receipt_date')
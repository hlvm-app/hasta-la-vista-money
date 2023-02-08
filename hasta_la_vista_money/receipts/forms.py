# import django_filters
from django import forms
from django.utils.translation import gettext_lazy
#
# from receipts.models import Customers


# class ReceiptsFilter(Form):
#     names_seller = Customers.objects.values_list('name_seller',
#                                                  'name_seller').distinct()
#     name_seller = django_filters.ChoiceFilter(label=gettext_lazy('Продавец'),
#                                               choices=names_seller)
#
#     class Meta:
#         model = Customers
#         fields = ('name_seller',)

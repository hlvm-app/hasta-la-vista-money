# import django_filters
from django.forms import ModelForm, formset_factory, DateTimeInput, DateInput
from django.utils.translation import gettext_lazy as _

from hasta_la_vista_money.receipts.models import Customer, Receipt, Product


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
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name_seller']
        labels = {
            'name_seller': _('Продавец')
        }


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'price', 'quantity', 'amount']
        labels = {
            'product_name': _('Наименование продукта'),
            'price': _('Цена'),
            'quantity': _('Количество'),
            'amount': _('Сумма')
        }


ProductFormSet = formset_factory(ProductForm, extra=1)


class ReceiptForm(ModelForm):
    class Meta:
        model = Receipt
        fields = ['receipt_date', 'operation_type', 'total_sum']
        labels = {
            'receipt_date': _('Дата и время чека'),
            'operation_type': _('Тип операции'),
            'total_sum': _('Итоговая сумма по чеку')
        }

    products = ProductFormSet()

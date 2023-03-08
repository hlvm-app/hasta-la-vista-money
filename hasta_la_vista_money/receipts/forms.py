import django_filters
from django.forms import (
    CharField,
    ModelForm,
    Select,
    TextInput,
    formset_factory,
)
from django.utils.translation import gettext_lazy as _
from hasta_la_vista_money.forms import BaseForm
from hasta_la_vista_money.receipts.models import Customer, Product, Receipt


class ReceiptFilter(django_filters.FilterSet):
    name_seller = django_filters.ModelChoiceFilter(
        queryset=Customer.objects.distinct(
            'name_seller',
        ).order_by(
            'name_seller',
        ),
        field_name='customer__name_seller',
        label=_('Продавец'),
    )
    receipt_date = django_filters.DateFromToRangeFilter(
        label=_('Период'),
        widget=django_filters.widgets.RangeWidget(
            attrs={
                'placeholder': _('YYYY-DD-MM'),
                'class': 'form-control',
            },
        ),
    )

    @property
    def qs(self):
        queryset = super().qs
        return queryset.distinct()

    class Meta:
        model = Receipt
        fields = ['name_seller', 'receipt_date']


class CustomerForm(BaseForm):
    labels = {
        'name_seller': _('Продавец'),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name_seller'].widget = Select(
            choices=self.get_name_seller_choices(),
        )

    @classmethod
    def get_name_seller_choices(cls):
        choices = [('', '--------'), ('other', _('Другой продавец'))]
        for seller in Customer.objects.order_by(  # noqa: WPS352
            'name_seller',
        ).values_list(
            'name_seller',
            flat=True,
        ).distinct():
            choices.append((seller, seller))
        return choices

    class Meta:
        model = Customer
        fields = ['name_seller']


class CustomerInputForm(ModelForm):
    name_seller = CharField(
        required=False,
        empty_value='',
        label=_('Продавец'),
        widget=TextInput(attrs={
            'class': 'name_seller_input',
        }),
    )

    class Meta:
        model = Customer
        fields = ['name_seller']


class ProductForm(BaseForm):
    labels = {
        'product_name': _('Наименование продукта'),
        'price': _('Цена'),
        'quantity': _('Количество'),
        'amount': _('Сумма'),
    }

    class Meta:
        model = Product
        fields = ['product_name', 'price', 'quantity', 'amount']


ProductFormSet = formset_factory(ProductForm, extra=1)


class ReceiptForm(BaseForm):
    labels = {
        'receipt_date': _('Дата и время чека'),
        'operation_type': _('Тип операции'),
        'total_sum': _('Итоговая сумма по чеку'),
    }

    class Meta:
        model = Receipt
        fields = ['receipt_date', 'operation_type', 'total_sum']

    products = ProductFormSet()

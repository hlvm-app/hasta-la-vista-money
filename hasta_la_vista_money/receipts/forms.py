import django_filters
from config.django.forms import BaseForm, DateTimePickerWidgetForm
from django.forms import (
    CharField,
    NumberInput,
    formset_factory,
    TextInput,
)
from django.utils.translation import gettext_lazy as _
from hasta_la_vista_money.receipts.models import Customer, Product, Receipt


class ReceiptFilter(django_filters.FilterSet):
    """Класс представляющий фильтр чеков на сайте."""

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
    """Класс формы продавца."""
    retail_place_address = CharField(
        label='Адрес места покупки',
        widget=TextInput(attrs={'placeholder': 'Поле может быть пустым'}),
    )
    retail_place = CharField(
        label='Имя продавца',
        widget=TextInput(attrs={'placeholder': 'Поле может быть пустым'}),
    )

    class Meta:
        model = Customer
        fields = ['name_seller', 'retail_place_address', 'retail_place']
        labels = {
            'name_seller': 'Имя продавца',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['retail_place_address'].required = False
        self.fields['retail_place'].required = False


class ProductForm(BaseForm):
    """Форма для внесения данных по продуктам."""

    labels = {
        'product_name': _('Наименование продукта'),
        'price': _('Цена'),
        'quantity': _('Количество'),
        'amount': _('Сумма'),
    }

    class Meta:
        model = Product
        fields = ['product_name', 'price', 'quantity', 'amount']
        widgets = {
            'price': NumberInput(attrs={'class': 'price'}),
            'quantity': NumberInput(attrs={'class': 'quantity'}),
            'amount': NumberInput(attrs={'class': 'amount', 'readonly': True}),
        }


ProductFormSet = formset_factory(ProductForm, extra=1)


class ReceiptForm(BaseForm):
    """Форма для внесения данных по чеку."""

    labels = {
        'account': _('Счёт'),
        'receipt_date': _('Дата и время чека'),
        'number_receipt': _('Номер документа'),
        'operation_type': _('Тип операции'),
        'total_sum': _('Итоговая сумма по чеку'),
    }

    class Meta:
        model = Receipt
        fields = [
            'customer',
            'account',
            'receipt_date',
            'number_receipt',
            'operation_type',
            'total_sum',
        ]
        widgets = {
            'receipt_date': DateTimePickerWidgetForm,
            'total_sum': NumberInput(
                attrs={'class': 'total-sum', 'readonly': True},
            ),
        }

    products = ProductFormSet()

import django_filters
from django.forms import (
    CharField,
    ModelChoiceField,
    NumberInput,
    Select,
    ValidationError,
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
        'existing_seller': _('Продавец'),
        'new_seller': _('Новый продавец'),
    }
    existing_seller = ModelChoiceField(
        queryset=Customer.objects.distinct(
            'name_seller',
        ).order_by(
            'name_seller',
        ),
        required=False,
        widget=Select(attrs={
            'id': 'id_existing_seller',
            'onchange': 'toggleNewSellerField()',
        }),
    )
    new_seller = CharField(
        required=False,
    )

    class Meta:
        model = Customer
        fields = ['existing_seller', 'new_seller']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['existing_seller'].initial = None
        self.fields[
            'existing_seller'
        ].choices = [('--', '-------'), ('other', 'Другой продавец')] + list(
            self.fields['existing_seller'].choices,
        )[1:]

    def clean(self):
        cleaned_data = super().clean()
        existing_seller = cleaned_data.get('existing_seller')
        new_seller = cleaned_data.get('new_seller')
        if not existing_seller and not new_seller:
            raise ValidationError(
                _(
                    'Пожалуйста, выберите существующего продавца или добавьте '
                    'нового.',  # noqa: WPS326
                ),
            )
        if existing_seller and new_seller:
            raise ValidationError(
                _(
                    'Пожалуйста, выберите только один вариант: '
                    'существующего продавца или ввод нового.',  # noqa: WPS326
                ),
            )
        return cleaned_data


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
        widgets = {
            'price': NumberInput(attrs={'class': 'price'}),
            'quantity': NumberInput(attrs={'class': 'quantity'}),
            'amount': NumberInput(attrs={'class': 'amount', 'readonly': True}),
        }


ProductFormSet = formset_factory(ProductForm, extra=1)


class ReceiptForm(BaseForm):
    labels = {
        'receipt_date': _('Дата и время чека'),
        'number_receipt': _('Номер документа'),
        'operation_type': _('Тип операции'),
        'total_sum': _('Итоговая сумма по чеку'),
    }

    class Meta:
        model = Receipt
        fields = [
            'receipt_date', 'number_receipt', 'operation_type', 'total_sum',
        ]
        widgets = {
            'total_sum': NumberInput(
                attrs={'class': 'total-sum', 'readonly': True}
            )
        }

    products = ProductFormSet()

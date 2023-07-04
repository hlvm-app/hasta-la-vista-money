import datetime

import django_filters
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from config.django.forms import BaseForm
from django.forms import (
    BooleanField,
    CharField,
    ModelChoiceField,
    NumberInput,
    Select,
    ValidationError,
    formset_factory,
)
from django.utils.translation import gettext_lazy as _

from hasta_la_vista_money import constants
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
        }),
    )
    new_seller = CharField(
        required=False,
    )
    add_new_seller = BooleanField(
        required=False,
        initial=False,
    )

    class Meta:
        model = Customer
        fields = ['existing_seller', 'new_seller', 'add_new_seller']

    def __init__(self, user, *args, **kwargs):
        """
        Инициализирующий класс-конструктор.

        Сначала мы инициализируем поле существующего продавца со значением None.
        Потом добавляем в начало выпадающего списка нужные поля и выводим
        список существующих продавцов.
        """
        self.user = user
        super().__init__(*args, **kwargs)
        existing_seller_field = self.fields['existing_seller']
        existing_seller_field.initial = None
        existing_seller_field.queryset = Customer.objects.filter(
            user=user,
        ).distinct(
            'name_seller',
        ).order_by(
            'name_seller',
        )
        existing_seller_field.widget.attrs['id'] = 'id_existing_seller'
        existing_seller_field.choices = [(
            '--', '-------',
        ), (
            'other', 'Другой продавец',
        )] + list(existing_seller_field.choices)[1:]

    def clean(self):
        """
        Переопределение метода для дополнительной валидации формы.

        :return cleaned_data: Очищенные данные.
        """
        cleaned_data = super().clean()
        existing_seller = cleaned_data.get('existing_seller')
        new_seller = cleaned_data.get('new_seller')
        add_new_seller = cleaned_data.get('add_new_seller')
        if not existing_seller and not new_seller and not add_new_seller:
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
        if add_new_seller and not new_seller:
            raise ValidationError(
                _(
                    'Пожалуйста, введите название нового продавца.',
                ),
            )
        if add_new_seller and new_seller:
            new_customer = Customer(
                user=self.user,
                name_seller=new_seller,
            )
            new_customer.save()
            new_customer.delete()
        return cleaned_data


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
            'account',
            'receipt_date',
            'number_receipt',
            'operation_type',
            'total_sum',
        ]
        widgets = {
            'receipt_date': DateTimePickerInput(
                options={
                    'format': 'DD/MM/YYYY HH:mm',
                    'showTodayButton': True,
                    'minDate': (
                            constants.TODAY.replace(
                                month=1, day=1, year=constants.TODAY.year - 1
                            ) - datetime.timedelta(days=1826)
                    ).strftime('%d/%m/%Y %H:%M'),
                    'maxDate': constants.TODAY.replace(
                        hour=23, minute=59, second=59
                    )
                },
            ),
        }

    products = ProductFormSet()

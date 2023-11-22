from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.forms import (
    CharField,
    DateTimeField,
    DecimalField,
    Form,
    ModelChoiceField,
    ModelForm,
    Textarea,
)
from hasta_la_vista_money.account.models import Account, TransferMoneyLog
from hasta_la_vista_money.commonlogic.forms import DateTimePickerWidgetForm
from hasta_la_vista_money.constants import MessageOnSite, NumericParameter


class AddAccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name_account', 'balance', 'currency']
        labels = {
            'name_account': 'Наименование счёта',
            'balance': 'Начальный баланс',
            'currency': 'Валюта счёта',
        }


class TransferMoneyAccountForm(Form):
    from_account = ModelChoiceField(label='Со счёта:', queryset=None)
    to_account = ModelChoiceField(label='На счёт:', queryset=None)
    exchange_date = DateTimeField(
        label='Дата перевода:',
        widget=DateTimePickerInput(),
    )
    amount = DecimalField(
        label='Сумма перевода:',
        max_digits=NumericParameter.TWENTY.value,
        decimal_places=NumericParameter.TWO.value,
    )
    notes = CharField(
        label='Заметка',
        required=False,
        widget=Textarea(
            attrs={
                'rows': 3,
                'placeholder': ''.join(
                    (
                        'Введите заметку не более 250 символов.\n',
                        'Поле необязательное!',
                    ),
                ),
            },
        ),
        max_length=NumericParameter.TWO_HUNDRED_FIFTY.value,
    )

    def __init__(self, user, *args, **kwargs):
        """
        Конструктов класса инициализирующий две поля формы.

        :param user:
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.fields['from_account'].queryset = Account.objects.filter(user=user)
        self.fields['to_account'].queryset = Account.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        from_account = cleaned_data.get('from_account')
        to_account = cleaned_data.get('to_account')
        amount = cleaned_data.get('amount')

        if from_account and to_account and from_account == to_account:
            self.add_error(
                'to_account',
                MessageOnSite.ANOTHER_ACCRUAL_ACCOUNT.value,
            )
        if from_account and amount and amount > from_account.balance:
            self.add_error(
                'from_account',
                MessageOnSite.SUCCESS_MESSAGE_INSUFFICIENT_FUNDS.value,
            )

        return cleaned_data

    def save(self, commit=True):
        from_account = self.cleaned_data['from_account']
        to_account = self.cleaned_data['to_account']
        amount = self.cleaned_data['amount']
        exchange_date = self.cleaned_data['exchange_date']
        notes = self.cleaned_data['notes']

        if from_account.transfer_money(to_account, amount):
            return TransferMoneyLog.objects.create(
                user=from_account.user,
                from_account=from_account,
                to_account=to_account,
                amount=amount,
                exchange_date=exchange_date,
                notes=notes,
            )

        return None

    class Meta:
        model = TransferMoneyLog
        fields = '__all__'
        widgets = {
            'date': DateTimePickerWidgetForm,
        }

from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.forms import (
    DateTimeField,
    DecimalField,
    Form,
    ModelChoiceField,
    ModelForm,
    ValidationError,
)
from hasta_la_vista_money.account.models import Account, TransferMoneyLog
from hasta_la_vista_money.constants import NumericParameter, MessageOnSite


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
    amount = DecimalField(
        label='Сумма перевода:',
        max_digits=NumericParameter.TWENTY.value,
        decimal_places=NumericParameter.TWO.value,
    )
    exchange_date = DateTimeField(
        label='Дата перевода:',
        widget=DateTimePickerInput(),
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_account'].queryset = Account.objects.filter(user=user)
        self.fields['to_account'].queryset = Account.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        from_account = cleaned_data['from_account']
        to_account = cleaned_data['to_account']

        if from_account == to_account:
            raise ValidationError(
                MessageOnSite.ANOTHER_ACCRUAL_ACCOUNT.value,
            )

        return cleaned_data

    def save(self, commit=True):
        from_account = self.cleaned_data['from_account']
        to_account = self.cleaned_data['to_account']
        amount = self.cleaned_data['amount']
        exchange_date = self.cleaned_data['exchange_date']
        print(from_account)
        print(to_account)

        if from_account.transfer_money(to_account, amount):
            return TransferMoneyLog.objects.create(
                user=from_account.user,
                from_account=from_account,
                to_account=to_account,
                amount=amount,
                exchange_date=exchange_date,
            )

        return None

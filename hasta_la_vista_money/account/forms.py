from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django import forms
from django.forms import ModelForm
from hasta_la_vista_money.account.models import Account, TransferMoneyLog
from hasta_la_vista_money.constants import NumericParameter


class AddAccountForm(ModelForm):

    class Meta:
        model = Account
        fields = ['name_account', 'balance', 'currency']
        labels = {
            'name_account': 'Наименование счёта',
            'balance': 'Начальный баланс',
            'currency': 'Валюта счёта',
        }


class TransferMoneyAccountForm(forms.Form):
    from_account = forms.ModelChoiceField(queryset=None)
    to_account = forms.ModelChoiceField(queryset=None)
    amount = forms.DecimalField(
        max_digits=NumericParameter.TWENTY.value,
        decimal_places=NumericParameter.TWO.value,
    )
    exchange_date = forms.DateTimeField(widget=DateTimePickerInput())

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_account'].queryset = Account.objects.filter(user=user)
        self.fields['to_account'].queryset = Account.objects.filter(user=user)

    def clean(self):
        cleanded_data = super().clean()
        from_account = cleanded_data['from_account']
        to_account = cleanded_data['to_account']

        if from_account == to_account:
            raise forms.ValidationError(
                'Вы не можете переводить с одинаково счёта'
            )
    def save(self, commit=True):
        from_account = self.cleaned_data['from_account']
        to_account = self.cleaned_data['to_account']
        amount = self.cleaned_data['amount']
        exchange_date = self.cleaned_data['exchange_date']

        if from_account.transfer_money(to_account, amount):
            transfer_log = TransferMoneyLog.objects.create(
                user=from_account.user,
                from_account=from_account,
                to_account=to_account,
                amount=amount,
                exchange_date=exchange_date,
            )
            return transfer_log

        return None

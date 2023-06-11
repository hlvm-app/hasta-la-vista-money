from django.forms import ModelForm
from hasta_la_vista_money.account.models import Account


class AddAccountForm(ModelForm):

    labels = {
        'name_account': 'Наименование счёта',
        'balance': 'Начальный баланс',
        'currency': 'Валюта счёта',
    }

    class Meta:
        model = Account
        fields = ['name_account', 'balance', 'currency']

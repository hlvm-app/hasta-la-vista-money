from hasta_la_vista_money.account.models import Account
from rest_framework import serializers

from hasta_la_vista_money.users.models import SelectedAccount


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name_account', 'balance', 'currency']


class SelectedAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectedAccount
        fields = ['__all__']

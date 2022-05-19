from django.forms import ModelForm
from django.utils.translation import gettext

from receipts.models import Receipt


class ReceiptForm(ModelForm):
    class Meta:
        model = Receipt
        fields = ('name_seller',)
        labels = {
            'name_seller': gettext('Продавец')
        }

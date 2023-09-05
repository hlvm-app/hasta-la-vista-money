"""Модуль форм по кредитам."""
from config.django.forms import BaseForm, DateTimePickerWidgetForm
from django.utils.translation import gettext_lazy as _
from hasta_la_vista_money.loan.models import Loan


class LoanForm(BaseForm):
    labels = {
        'date': _('Начальная дата кредита'),
        'loan_amount': _('Сумма кредита'),
        'annual_interest_rate': _('Годовая ставка в %'),
        'period_loan': _('Срок кредита в месяцах'),
    }

    class Meta:
        model = Loan
        fields = ['date', 'loan_amount', 'annual_interest_rate', 'period_loan']
        widgets = {
            'date': DateTimePickerWidgetForm,
        }

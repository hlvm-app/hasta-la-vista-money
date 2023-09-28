"""Модуль форм по кредитам."""
from config.django.forms import BaseForm, DateTimePickerWidgetForm
from django.utils.translation import gettext_lazy as _
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.loan.models import Loan, PaymentMakeLoan


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


class PaymentMakeLoanForm(BaseForm):
    labels = {
        'date': _('Дата платежа'),
        'account': _('Счёт списания'),
        'loan': _('Кредит'),
        'amount': _('Сумма платежа'),
    }

    def __init__(self, user, *args, **kwargs):
        """
        Исключаем из выборки счетов все счета кредитов.

        :param user:
        """
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['account'].queryset = self.get_account_queryset()

    def get_account_queryset(self):
        accounts = Account.objects.filter(user=self.user)

        loan = Loan.objects.filter(user=self.user).values_list(
            'account',
            flat=True,
        )
        return accounts.exclude(id__in=loan)

    class Meta:
        model = PaymentMakeLoan
        fields = ['date', 'account', 'loan', 'amount']
        widgets = {
            'date': DateTimePickerWidgetForm,
        }

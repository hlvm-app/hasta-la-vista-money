from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.constants import MessageOnSite
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin
from hasta_la_vista_money.loan.forms import LoanForm, PaymentMakeLoanForm
from hasta_la_vista_money.loan.models import (
    Loan,
    PaymentMakeLoan,
    PaymentSchedule,
)
from hasta_la_vista_money.loan.tasks import async_calculate_annuity_loan
from hasta_la_vista_money.users.models import User


class LoanView(CustomNoPermissionMixin, SuccessMessageMixin, TemplateView):
    template_name = 'loan/loan.html'
    no_permission_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(
            username=request.user,
        )
        if user:
            loan_form = LoanForm()
            payment_make_loan_form = PaymentMakeLoanForm(user=request.user)
            loan = Loan.objects.filter(user=request.user).all()
            result_calculate = (
                PaymentSchedule.objects.select_related('loan')
                .filter(
                    user=request.user,
                )
                .all()
            )
            payment_make_loan = PaymentMakeLoan.objects.filter(
                user=request.user,
            ).all()
            return render(
                request,
                self.template_name,
                {
                    'loan_form': loan_form,
                    'payment_make_loan_form': payment_make_loan_form,
                    'loan': loan,
                    'result_calculate': result_calculate,
                    'payment_make_loan': payment_make_loan,
                },
            )


class LoanCreateView(SuccessMessageMixin, CreateView):
    template_name = 'loan/loan.html'
    model = Loan
    form_class = LoanForm
    success_url = reverse_lazy('loan:list')
    success_message = 'Кредит успешно добавлен'

    def post(self, request, *args, **kwargs):
        loan_form = LoanForm(request.POST)

        if loan_form.is_valid():
            loan = loan_form.save(commit=False)
            loan.user = request.user
            date = loan_form.cleaned_data.get('date')
            loan_amount = loan_form.cleaned_data.get('loan_amount')
            annual_interest_rate = loan_form.cleaned_data.get(
                'annual_interest_rate',
            )
            period_loan = loan_form.cleaned_data.get('period_loan')
            loan.account = Account.objects.create(
                user=request.user,
                name_account=f'Кредитный счёт на {loan_amount}',
                balance=loan_amount,
                currency='RU',
            )
            loan.save()
            async_calculate_annuity_loan(
                request.user,
                loan,
                date,
                loan_amount,
                annual_interest_rate,
                period_loan,
            )
            response_data = {'success': True}
        else:
            response_data = {
                'success': False,
                'errors': loan_form.errors,
            }
        return JsonResponse(response_data)


class PaymentMakeView(CreateView):
    template_name = 'loan/loan.html'
    model = PaymentMakeLoan
    form_class = PaymentMakeLoanForm
    success_url = reverse_lazy('loan:list')

    def post(self, request, *args, **kwargs):
        payment_make_form = self.form_class(request.POST)
        response_data = {}
        if payment_make_form.is_valid():
            payment_make = payment_make_form.save(commit=False)
            amount = payment_make_form.cleaned_data.get('amount')
            account = payment_make_form.cleaned_data.get('account')
            selected_account = get_object_or_404(Account, id=account.id)
            if selected_account.user == request.user:
                selected_account.balance -= amount
                selected_account.save()
                payment_make.user = request.user
                payment_make.save()
                messages.success(
                    request,
                    MessageOnSite.SUCCESS_MESSAGE_PAYMENT_MAKE.value,
                )
                response_data = {'success': True}

        else:
            response_data = {
                'success': False,
                'errors': payment_make_form.errors,
            }
        return JsonResponse(response_data)

from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin
from hasta_la_vista_money.loan.forms import LoanForm
from hasta_la_vista_money.loan.models import Loan
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
            loan = Loan.objects.filter(user=request.user).all()
            result_calculate = []
            for item_loan in loan:
                result_calculate.append(
                    async_calculate_annuity_loan(
                        item_loan.pk,
                        item_loan.date,
                        item_loan.loan_amount,
                        item_loan.annual_interest_rate,
                        item_loan.period_loan,
                    ),
                )

            return render(
                request,
                self.template_name,
                {
                    'loan_form': loan_form,
                    'loan': loan,
                    'result_calculate': result_calculate,
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
            loan_amount = loan_form.cleaned_data.get('loan_amount')
            loan.account = Account.objects.create(
                user=request.user,
                name_account=f'Кредитный счёт на {loan_amount}',
                balance=loan_amount,
                currency='RU',
            )
            loan.save()
            response_data = {'success': True}
        else:
            response_data = {
                'success': False,
                'errors': loan_form.errors,
            }
        return JsonResponse(response_data)

    def calculate_annuity_loan(self):
        ...

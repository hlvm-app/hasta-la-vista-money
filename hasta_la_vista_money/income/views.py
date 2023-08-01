from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView
from django.views.generic.edit import CreateView, DeletionMixin
from django_filters.views import FilterView
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.constants import (
    MessageOnSite,
    SuccessUrlView,
    TemplateHTMLView,
)
from hasta_la_vista_money.custom_mixin import (
    CustomNoPermissionMixin,
    DeleteCategoryMixin,
    ExpenseIncomeFormValidCreateMixin,
)
from hasta_la_vista_money.income.forms import AddCategoryIncomeForm, IncomeForm
from hasta_la_vista_money.income.models import Income, IncomeType


class IncomeView(CustomNoPermissionMixin, SuccessMessageMixin, FilterView):
    """Представление просмотра доходов из модели, на сайте."""

    model = Income
    template_name = TemplateHTMLView.INCOME_TEMPLATE.value
    context_object_name = 'incomes'
    no_permission_url = reverse_lazy('login')
    success_url = SuccessUrlView.INCOME_URL.value

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            income_form = IncomeForm()
            add_category_income_form = AddCategoryIncomeForm()

            income_form.fields['account'].queryset = Account.objects.filter(
                user=request.user,
            )

            income_by_month = Income.objects.filter(
                user=request.user,
            ).values(
                'id',
                'date',
                'account__name_account',
                'category__name',
                'amount',
            ).order_by('-date')

            categories = IncomeType.objects.filter(user=request.user).all()

            return render(
                request,
                self.template_name,
                {
                    'add_category_income_form': add_category_income_form,
                    'categories': categories,
                    'income_by_month': income_by_month,
                    'income_form': income_form,
                },
            )


class IncomeCreateView(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    CreateView,
):
    model = Income
    template_name = TemplateHTMLView.INCOME_TEMPLATE.value
    no_permission_url = reverse_lazy('login')
    form_class = IncomeForm
    success_url = reverse_lazy(SuccessUrlView.INCOME_URL.value)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper.form_action = reverse_lazy('income:create')
        return form

    def post(self, request, *args, **kwargs):
        income_form = IncomeForm(request.POST)
        response_data = {}

        if income_form.is_valid():
            income = income_form.save(commit=False)
            amount = income_form.cleaned_data.get('amount')
            account = income_form.cleaned_data.get('account')
            account_balance = get_object_or_404(Account, id=account.id)

            if account_balance.user == request.user:
                account_balance.balance += amount
                account_balance.save()
                income.user = request.user
                income.save()
                messages.success(
                    request, MessageOnSite.SUCCESS_INCOME_ADDED.value,
                )
                response_data = {'success': True}
        else:
            response_data = {
                'success': False, 'errors': income_form.errors,
            }
        return JsonResponse(response_data)


class IncomeUpdateView(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = Income
    template_name = 'income/change_income.html'
    form_class = IncomeForm
    no_permission_url = reverse_lazy('login')
    success_url = reverse_lazy(SuccessUrlView.INCOME_URL.value)

    def get(self, request, *args, **kwargs):
        income = self.get_object()
        income_form = IncomeForm(instance=income)
        return render(
            request,
            self.template_name,
            {'income_form': income_form},
        )

    def form_valid(self, form):
        income_id = self.get_object().id
        if income_id:
            income = get_object_or_404(Income, id=income_id)
        else:
            income = form.save(commit=False)

        amount = form.cleaned_data.get('amount')
        account = form.cleaned_data.get('account')
        account_balance = get_object_or_404(Account, id=account.id)

        if account_balance.user == self.request.user:
            if income_id:
                old_amount = income.amount
                account_balance.balance -= old_amount
            account_balance.balance += amount
            account_balance.save()

            income.user = self.request.user
            income.amount = amount
            income.save()
            messages.success(
                self.request,
                MessageOnSite.SUCCESS_INCOME_UPDATE.value,
            )
            return super().form_valid(form)


class IncomeDeleteView(DeleteView, DeletionMixin):
    model = Income
    template_name = TemplateHTMLView.INCOME_TEMPLATE.value
    context_object_name = 'incomes'
    no_permission_url = reverse_lazy('login')
    success_url = reverse_lazy(SuccessUrlView.INCOME_URL.value)

    def form_valid(self, form):
        income = self.get_object()
        account = income.account
        amount = income.amount
        account_balance = get_object_or_404(Account, id=account.id)

        if account_balance.user == self.request.user:
            account_balance.balance -= amount
            account_balance.save()
            messages.success(
                self.request, MessageOnSite.SUCCESS_INCOME_DELETED.value,
            )
            return super().form_valid(form)


class IncomeCategoryCreateView(ExpenseIncomeFormValidCreateMixin):
    model = IncomeType
    template_name = TemplateHTMLView.INCOME_TEMPLATE.value
    success_url = reverse_lazy(SuccessUrlView.INCOME_URL.value)
    form_class = AddCategoryIncomeForm


class IncomeCategoryDeleteView(DeleteCategoryMixin):
    model = IncomeType
    success_url = reverse_lazy(SuccessUrlView.INCOME_URL.value)

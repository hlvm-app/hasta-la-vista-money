from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import CreateView, FormView, ListView
from hasta_la_vista_money.income.forms import IncomeForm
from hasta_la_vista_money.income.models import Income


class IncomeView(LoginRequiredMixin, ListView):
    model = Income
    template_name = 'income/income.html'
    context_object_name = 'incomes'
    error_message = gettext_lazy(
        'У вас нет прав на просмотр данной страницы! Авторизуйтесь!',
    )
    no_permission_url = 'login'


class AddIncome(LoginRequiredMixin, CreateView, FormView):
    model = Income
    form_class = IncomeForm
    template_name = 'income/add_income.html'
    success_url = reverse_lazy('income:list')

    def get(self, request, *args, **kwargs):
        income_form = IncomeForm()
        return self.render_to_response({'income_form': income_form})

    def post(self, request, *args, **kwargs):
        income_form = IncomeForm(request.POST)
        if income_form.is_valid():
            income_form.save()
            return redirect(reverse_lazy('income:list'))
        else:
            return self.render_to_response(  # noqa: WPS503
                {'income_form': income_form},
            )

from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView
from hasta_la_vista_money.constants import Messages
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin
from hasta_la_vista_money.income.forms import IncomeForm
from hasta_la_vista_money.income.models import Income


class IncomeView(CustomNoPermissionMixin, ListView):
    """Представление просмотра доходов из модели, на сайте."""

    model = Income
    template_name = 'income/income.html'
    context_object_name = 'incomes'
    permission_denied_message = Messages.ACCESS_DENIED.value
    no_permission_url = reverse_lazy('login')


class AddIncome(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    CreateView,
    FormView,
):
    """Класс отвечающий за добавление данных в базу по доходам."""

    model = Income
    form_class = IncomeForm
    template_name = 'income/add_income.html'
    permission_denied_message = Messages.ACCESS_DENIED.value
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

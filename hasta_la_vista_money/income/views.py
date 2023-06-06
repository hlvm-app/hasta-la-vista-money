from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django_filters.views import FilterView
from hasta_la_vista_money.constants import Messages
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin
from hasta_la_vista_money.income.forms import IncomeForm
from hasta_la_vista_money.income.models import Income


class IncomeView(CustomNoPermissionMixin, SuccessMessageMixin, FilterView):
    """Представление просмотра доходов из модели, на сайте."""

    model = Income
    template_name = 'income/income.html'
    context_object_name = 'incomes'
    permission_denied_message = Messages.ACCESS_DENIED.value
    no_permission_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        sort_by_month = Income.objects.all().order_by('-date')
        return render(
            request, self.template_name, {'income_by_month': sort_by_month},
        )

    def post(self, request):
        if 'delete_income_button' in request.POST:
            id_income = request.POST.get('income_id')
            income = get_object_or_404(self.model, pk=id_income)
            income.delete()
        return self.get(request)


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

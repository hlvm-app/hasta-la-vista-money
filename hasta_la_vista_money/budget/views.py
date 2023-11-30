from django.views.generic import ListView
from hasta_la_vista_money.budget.forms import SelectDateForm
from hasta_la_vista_money.budget.models import Planning


class BaseView(ListView):
    template_name = 'budget.html'


class BudgetView(BaseView):
    model = Planning

    def get_context_data(self, *, object_list=None, **kwargs):
        select_date_form = SelectDateForm(initial={'select_date': '----------'})

        context = super().get_context_data(**kwargs)
        context['select_date_form'] = select_date_form

        return context

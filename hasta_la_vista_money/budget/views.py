from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.views.generic import ListView
from hasta_la_vista_money.budget.models import DateList, Planning
from hasta_la_vista_money.expense.models import Expense


class BaseView(ListView):
    template_name = 'budget.html'


class BudgetView(BaseView):
    model = Planning

    def get_context_data(self, *, object_list=None, **kwargs):
        list_date = DateList.objects.filter(user=self.request.user).order_by(
            'date',
        )
        queryset_expense = (
            Expense.objects.filter(user=self.request.user)
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total_amount=Sum('amount'))
        )

        context = super().get_context_data(**kwargs)
        context['queryset_expense'] = queryset_expense
        context['list_date'] = list_date

        return context

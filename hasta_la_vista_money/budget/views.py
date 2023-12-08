from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from hasta_la_vista_money.budget.models import DateList, Planning
from hasta_la_vista_money.commonlogic.generate_dates import generate_date_list
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin
from hasta_la_vista_money.expense.models import Expense, ExpenseCategory
from hasta_la_vista_money.users.models import User


class BaseView:
    template_name = 'budget.html'


class BudgetView(CustomNoPermissionMixin, BaseView, ListView):
    model = Planning

    def get_context_data(self, **kwargs):  # noqa: WPS210
        context = super().get_context_data(**kwargs)

        list_dates = DateList.objects.filter(user=self.request.user).order_by(
            'date',
        )

        parent_categories = ExpenseCategory.objects.filter(
            user=self.request.user,
            parent_category=None,
        ).order_by('name')

        expenses_dict = {}
        for category in parent_categories:
            expenses_dict[category.name] = {}

            queryset_expense = (
                Expense.objects.filter(
                    user=self.request.user,
                    category__parent_category=category,
                )
                .annotate(month=TruncMonth('date'))
                .values('month')
                .annotate(total_amount=Sum('amount'))
                .order_by('month')
            )

            for expense in queryset_expense:
                month_key = expense['month'].strftime('%Y-%m')
                total_amount = expense['total_amount']
                expenses_dict[category.name][month_key] = total_amount

        category_amount = []
        total_sums = [0] * len(list_dates)  # noqa: WPS435
        for category in parent_categories:
            row = {'category': category.name, 'amounts': []}

            for date_index, date in enumerate(list_dates):
                month_key = date.date.strftime('%Y-%m')
                amount = expenses_dict.get(category.name, {}).get(
                    month_key,
                    '0,00',
                )
                row['amounts'].append(amount)
                amount_str = str(amount)
                total_sums[date_index] += float(amount_str.replace(',', '.'))

            category_amount.append(row)
        context['list_dates'] = list_dates
        context['category_amount'] = category_amount
        context['total_sums'] = total_sums

        return context


def generate_date_list_view(request):
    """Функция представления генерации дат."""
    if request.method == 'POST':
        user = request.user
        queryset_user = get_object_or_404(User, username=user)
        queryset_last_date = queryset_user.budget_date_list_users.last().date
        generate_date_list(queryset_last_date, queryset_user)
        return redirect(reverse_lazy('budget:list'))

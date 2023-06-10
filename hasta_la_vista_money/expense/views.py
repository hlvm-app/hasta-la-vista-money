from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from hasta_la_vista_money.constants import MessageOnSite
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin
from hasta_la_vista_money.receipts.models import Receipt


class ExpenseView(CustomNoPermissionMixin, SuccessMessageMixin, View):
    model = Receipt
    template_name = 'expense/expense.html'
    context_object_name = 'expense'
    permission_denied_message = MessageOnSite.ACCESS_DENIED.value
    no_permission_url = reverse_lazy('login')

    def get(self, request):
        """
        Метод отображения расходов по месяцам на странице.

        :param request: Запрос данных со страницы сайта.
        :return: Рендеринг данных на странице сайта.
        """
        group_by_months = Receipt.objects.annotate(
            month=TruncMonth('receipt_date'),
        ).values(
            'month',
        ).annotate(
            c=Count('id'),
            total_amount=Sum('total_sum'),
        ).order_by('-month')
        return render(request, self.template_name, {
            'expense_by_months': group_by_months,
        })

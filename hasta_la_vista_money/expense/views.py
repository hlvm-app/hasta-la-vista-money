from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views import View
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth


from hasta_la_vista_money.receipts.models import Receipt


class ExpenseView(LoginRequiredMixin, View, SuccessMessageMixin):
    model = Receipt
    template_name = 'expense/expense.html'
    context_object_name = 'expense'
    error_message = gettext_lazy('У вас нет прав на просмотр данной страницы! '
                                 'Авторизуйтесь!')
    no_permission_url = reverse_lazy('login')

    def get(self, request):
        group_by_months = Receipt.objects.annotate(
            month=TruncMonth('receipt_date')
        ).values(
            'month'
        ).annotate(
            c=Count('id'),
            total_amount=Sum('total_sum')
        )
        return render(request, self.template_name, {'months': group_by_months})

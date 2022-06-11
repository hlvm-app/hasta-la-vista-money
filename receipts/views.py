from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import FormView
from django_filters.views import FilterView
from django_filters import rest_framework as filters

from receipts.forms import ReceiptsFilter, AddReceiptForm
from receipts.models import Receipt


class ReceiptView(LoginRequiredMixin, SuccessMessageMixin, FilterView):
    model = Receipt
    template_name = 'receipts/receipts.html'
    context_object_name = 'receipts'
    ordering = ['-receipt_date']
    filterset_class = ReceiptsFilter
    filter_backends = (filters.DjangoFilterBackend,)

    error_message = gettext_lazy('У вас нет прав на просмотр данной страницы! '
                                 'Авторизуйтесь!')
    no_permission_url = 'login'

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.no_permission_url)


class AddReceiptView(LoginRequiredMixin, FormView):
    model = Receipt
    form_class = AddReceiptForm
    template_name = 'receipts/add_receipt.html'
    success_url = reverse_lazy('receipts:list')

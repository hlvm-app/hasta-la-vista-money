from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import CreateView
from django.views.generic.edit import FormMixin

from .forms import ReceiptForm
from .models import Receipt


class ReceiptView(LoginRequiredMixin, View, SuccessMessageMixin):
    template_name = 'receipts/receipts.html'
    model = Receipt
    context_object_name = 'receipts'
    error_message = gettext_lazy('У вас нет прав на просмотр данной страницы! '
                                 'Авторизуйтесь!')
    no_permission_url = reverse_lazy('login')

    def get(self, request):
        receipts = Receipt.objects.all()
        return render(request, self.template_name, {'receipts': receipts})

    def post(self, request):
        if 'delete_button' in request.POST:
            receipt_id = request.POST.get('receipt_id')
            receipt = get_object_or_404(self.model, pk=receipt_id)
            for product in receipt.product.all():
                product.delete()
            receipt.customer.delete()
            receipt.delete()
        return self.get(request)


class CreateReceiptView(LoginRequiredMixin, CreateView, FormMixin):
    model = Receipt
    template_name = 'receipts/create_customer.html'
    form_class = ReceiptForm
    success_url = reverse_lazy('receipts:list')
    error_message = gettext_lazy('У вас нет прав на просмотр данной страницы! '
                                 'Авторизуйтесь!')
    no_permission_url = reverse_lazy('login')

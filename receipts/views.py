from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy

from .models import Receipt


class ReceiptView(ListView, LoginRequiredMixin, SuccessMessageMixin):
    template_name = 'receipts/receipts.html'
    model = Receipt
    error_message = gettext_lazy('У вас нет прав на просмотр данной страницы! '
                                 'Авторизуйтесь!')
    no_permission_url = reverse_lazy('login')
    
    def get(self, request):
        receipts = Receipt.objects.all()
        return render(request, self.template_name, {'receipts': receipts}).
    
    def post(self, request):
        if 'delete_button' in request.POST:
            receipt_id = request.POST.get('receipt_id')
            receipt = get_object_or_404(self.model, pk=receipt_id)
            for product in receipt.product.all():
                product.delete()
            receipt.customer.delete()
            receipt.delete()
        return self.get(request)
    
    
# def receipt_view(request):
#     receipts = Receipt.objects.all()
#     if request.method == "POST" and 'delete_button' in request.POST:
#         receipt_id = request.POST.get('receipt_id')
#         receipt = get_object_or_404(Receipt, pk=receipt_id)
#         for product in receipt.product.all():
#             product.delete()
#         receipt.customer.delete()
#         receipt.delete()
#     return render(request, 'receipts/receipts.html', {'receipts': receipts})

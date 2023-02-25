from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import CreateView

from .forms import CustomerForm, ReceiptForm, ProductFormSet
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


class ReceiptCreateView(CreateView):
    model = Receipt
    template_name = 'receipts/create_receipt.html'
    success_url = 'receipts:list'

    def get(self, request, *args, **kwargs):
        seller_form = CustomerForm()
        receipt_form = ReceiptForm()
        product_formset = ProductFormSet()
        return self.render_to_response({
            'seller_form': seller_form,
            'receipt_form': receipt_form,
            'product_formset': product_formset})

    def post(self, request, *args, **kwargs):
        seller_form = CustomerForm(request.POST)
        receipt_form = ReceiptForm(request.POST)
        product_formset = ProductFormSet(request.POST)
        if seller_form.is_valid() and receipt_form.is_valid() and \
                product_formset.is_valid():
            seller = seller_form.save()
            receipt = receipt_form.save(commit=False)
            receipt.customer = seller
            receipt.save()
            for product_form in product_formset:
                product = product_form.save()
                receipt.product.add(product)
            return redirect(reverse_lazy("receipts:list"))
        else:
            return self.render_to_response({
                'seller_form': seller_form,
                'receipt_form': receipt_form,
                'product_formset': product_formset
            })

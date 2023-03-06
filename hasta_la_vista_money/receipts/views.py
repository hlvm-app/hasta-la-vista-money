from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import CreateView
from django_filters import rest_framework as filters
from django_filters.views import FilterView

from .forms import CustomerForm, ReceiptForm, ProductFormSet, ReceiptFilter, \
    CustomerInputForm
from .models import Receipt


class ReceiptView(LoginRequiredMixin, SuccessMessageMixin, FilterView):
    template_name = 'receipts/receipts.html'
    model = Receipt
    context_object_name = 'receipts'
    filterset_class = ReceiptFilter
    filter_backends = (filters.DjangoFilterBackend,)
    error_message = gettext_lazy('У вас нет прав на просмотр данной страницы! '
                                 'Авторизуйтесь!')
    no_permission_url = reverse_lazy('login')

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
        customer_input_form = CustomerInputForm()
        receipt_form = ReceiptForm()
        product_formset = ProductFormSet()

        return self.render_to_response({
            'seller_form': seller_form,
            'customer_input_form': customer_input_form,
            'receipt_form': receipt_form,
            'product_formset': product_formset})

    def post(self, request, *args, **kwargs):

        seller_form = CustomerForm(request.POST)
        customer_input_form = CustomerInputForm(request.POST)
        receipt_form = ReceiptForm(request.POST)
        product_formset = ProductFormSet(request.POST)

        if seller_form.is_valid() and customer_input_form.is_valid() \
                and receipt_form.is_valid() and product_formset.is_valid():
            seller = seller_form.save()
            seller_input = customer_input_form.save()
            receipt = receipt_form.save(commit=False)

            if seller is None:
                receipt.customer = seller_input
            receipt.customer = seller
            receipt.save()

            for product_form in product_formset:
                product = product_form.save()
                receipt.product.add(product)
            return redirect(reverse_lazy("receipts:list"))
        else:
            return self.render_to_response({
                'seller_form': seller_form,
                'customer_input_form': customer_input_form,
                'receipt_form': receipt_form,
                'product_formset': product_formset
            })

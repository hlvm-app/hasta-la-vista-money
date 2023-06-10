from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django_filters.views import FilterView
from hasta_la_vista_money.constants import MessageOnSite, ReceiptConstants
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin
from hasta_la_vista_money.receipts.forms import (
    CustomerForm,
    ProductFormSet,
    ReceiptForm,
)
from hasta_la_vista_money.receipts.models import Customer, Receipt


class ReceiptView(CustomNoPermissionMixin, SuccessMessageMixin, FilterView):
    """Класс представления чека на сайте."""

    template_name = 'receipts/receipts.html'
    model = Receipt
    context_object_name = 'receipts'
    ordering = ['-receipt_date']
    permission_denied_message = MessageOnSite.ACCESS_DENIED.value
    no_permission_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        receipts = Receipt.objects.filter(
            user=request.user,
        )
        return render(request, self.template_name, {'receipts': receipts})

    def post(self, request):
        if 'delete_receipt_button' in request.POST:
            receipt_id = request.POST.get('receipt_id')
            receipt = get_object_or_404(self.model, pk=receipt_id)

            for product in receipt.product.all():
                product.delete()

            receipt.customer.delete()
            receipt.delete()
        return self.get(request)


class ReceiptCreateView(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    CreateView,
):
    """Класс для преставления формы создания чека на сайте."""

    model = Receipt
    template_name = 'receipts/create_receipt.html'
    success_url = 'receipts:list'
    permission_denied_message = MessageOnSite.ACCESS_DENIED.value
    no_permission_url = reverse_lazy('login')
    success_message = MessageOnSite.SUCCESS_MESSAGE_CREATE_RECEIPT.value

    def get(self, request, *args, **kwargs):
        existing_sellers = Customer.objects.all()
        seller_form = CustomerForm()
        seller_form.fields['existing_seller'].queryset = existing_sellers
        receipt_form = ReceiptForm()
        product_formset = ProductFormSet()
        return self.render_to_response({
            'seller_form': seller_form,
            'receipt_form': receipt_form,
            'product_formset': product_formset,
        })

    @classmethod
    def get_or_create_seller(cls, seller_form):
        existing_seller = seller_form.cleaned_data.get('existing_seller')
        new_seller = seller_form.cleaned_data.get('new_seller')
        if existing_seller:
            seller = existing_seller
        elif new_seller:
            seller = Customer.objects.create(name_seller=new_seller)
        else:
            seller = None
        return seller

    @classmethod
    def create_receipt(cls, receipt_form, product_formset, seller):
        receipt = receipt_form.save(commit=False)
        receipt.customer = seller
        receipt.save()
        for product_form in product_formset:
            product = product_form.save()
            receipt.product.add(product)
        return receipt

    @classmethod
    def check_exist_receipt(cls, receipt_form):
        number_receipt = receipt_form.cleaned_data.get('number_receipt')
        return Receipt.objects.filter(number_receipt=number_receipt)

    def post(self, request, *args, **kwargs):
        seller_form = CustomerForm(request.POST)
        receipt_form = ReceiptForm(request.POST)
        product_formset = ProductFormSet(request.POST)

        if (
            seller_form.is_valid() and receipt_form.is_valid() and
            product_formset.is_valid()
        ):
            seller = self.get_or_create_seller(seller_form)

            number_receipt = self.check_exist_receipt(receipt_form)
            if number_receipt:
                messages.error(
                    request, ReceiptConstants.RECEIPT_ALREADY_EXISTS.value,
                )
            elif seller:
                self.create_receipt(receipt_form, product_formset, seller)
                return redirect(reverse_lazy('receipts:list'))

        return self.render_to_response(
            {
                'seller_form': seller_form,
                'receipt_form': receipt_form,
                'product_formset': product_formset,
            },
        )

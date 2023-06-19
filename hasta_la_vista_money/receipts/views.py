from typing import Any, Dict

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.constants import MessageOnSite, ReceiptConstants
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin
from hasta_la_vista_money.receipts.forms import (
    CustomerForm,
    ProductFormSet,
    ReceiptForm,
)
from hasta_la_vista_money.receipts.models import Customer, Receipt


class ReceiptView(CustomNoPermissionMixin, SuccessMessageMixin, TemplateView):
    """Класс представления чека на сайте."""

    template_name = 'receipts/receipts.html'
    model = Receipt
    context_object_name = 'receipts'
    ordering = ['-receipt_date']
    success_url = 'receipts:list'
    permission_denied_message = MessageOnSite.ACCESS_DENIED.value
    no_permission_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        if request.user:
            existing_sellers = Customer.objects.filter(user=request.user)
            seller_form = CustomerForm(user=request.user)
            seller_form.fields['existing_seller'].queryset = existing_sellers
            receipt_form = ReceiptForm()
            receipt_form.fields['account'].queryset = Account.objects.filter(
                user=request.user,
            )
            product_formset = ProductFormSet()
            receipts = Receipt.objects.filter(
                user=request.user,
            )
            return render(request, self.template_name, {
                'receipts': receipts,
                'seller_form': seller_form,
                'receipt_form': receipt_form,
                'product_formset': product_formset,
            })

    @classmethod
    def get_or_create_seller(cls, request, seller_form):
        existing_seller = Customer.objects.filter(user=request.user)
        new_seller = seller_form.cleaned_data.get('new_seller')
        if existing_seller:
            seller = existing_seller
        elif new_seller:
            seller = Customer.objects.create(
                user=request.user,
                name_seller=new_seller,
            )
        else:
            seller = None
        return seller

    @classmethod
    def create_receipt(cls, request, receipt_form, product_formset, seller):
        receipt = receipt_form.save(commit=False)
        total_sum = receipt.total_sum
        account = receipt.account
        account_balance = get_object_or_404(Account, id=account.id)
        if account_balance.user == request.user:
            account_balance.balance -= total_sum
            account_balance.save()
            receipt.user = request.user
            receipt.customer = seller
            receipt.save()
            for product_form in product_formset:
                product = product_form.save(commit=False)
                product.user = request.user
                product.save()
                receipt.product.add(product)
            return receipt

    @classmethod
    def check_exist_receipt(cls, request, receipt_form):
        number_receipt = receipt_form.cleaned_data.get('number_receipt')
        return Receipt.objects.filter(
            user=request.user, number_receipt=number_receipt,
        )

    def post(self, request, *args, **kwargs) -> Dict[str, Any]:  # noqa: WPS231 C901 E501
        if 'delete_receipt_button' in request.POST:
            receipt_id = request.POST.get('receipt_id')
            receipt = get_object_or_404(self.model, pk=receipt_id)
            account = receipt.account
            total_sum = receipt.total_sum
            account_balance = get_object_or_404(Account, id=account.id)

            if account_balance.user == request.user:
                account_balance.balance += total_sum
                account_balance.save()
                for product in receipt.product.all():
                    product.delete()

                receipt.customer.delete()

                receipt.delete()
                return redirect(reverse_lazy(self.success_url))

        seller_form = CustomerForm(request.user, request.POST)
        receipt_form = ReceiptForm(request.POST)
        product_formset = ProductFormSet(request.POST)

        if (
            receipt_form.is_valid() and
            product_formset.is_valid() and
            seller_form.is_valid()
        ):
            seller = self.get_or_create_seller(request, seller_form)
            number_receipt = self.check_exist_receipt(request, receipt_form)
            if number_receipt:
                messages.error(
                    request, ReceiptConstants.RECEIPT_ALREADY_EXISTS.value,
                )
            elif seller:
                self.create_receipt(
                    request,
                    receipt_form,
                    product_formset,
                    seller[0],
                )
                return redirect(reverse_lazy(self.success_url))

        return self.render_to_response(
            {
                'seller_form': seller_form,
                'receipt_form': receipt_form,
                'product_formset': product_formset,
            },
        )

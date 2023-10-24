from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, ProtectedError, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.commonlogic.custom_paginator import (
    paginator_custom_view,
)
from hasta_la_vista_money.constants import (
    MessageOnSite,
    ReceiptConstants,
    SuccessUrlView,
    TemplateHTMLView,
)
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin
from hasta_la_vista_money.receipts.forms import (
    CustomerForm,
    ProductFormSet,
    ReceiptForm,
)
from hasta_la_vista_money.receipts.models import Customer, Receipt
from hasta_la_vista_money.users.models import User


class ReceiptView(CustomNoPermissionMixin, SuccessMessageMixin, ListView):
    """Класс представления чека на сайте."""

    paginate_by = 10
    template_name = 'receipts/receipts.html'
    model = Receipt
    context_object_name = 'receipts'
    no_permission_url = reverse_lazy('login')
    success_url = 'receipts:list'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user)
        if user.is_authenticated:
            seller_form = CustomerForm()

            receipt_form = ReceiptForm()
            receipt_form.fields['account'].queryset = user.account_users
            receipt_form.fields[
                'customer'
            ].queryset = user.customer_users.distinct('name_seller')

            product_formset = ProductFormSet()
            receipts = user.receipt_users.prefetch_related(
                'product',
            ).select_related('customer')

            page_receipts = paginator_custom_view(
                request,
                receipts,
                self.paginate_by,
                'receipts',
            )

            list_receipts = Receipt.objects.prefetch_related('product').all()
            purchased_products = (
                list_receipts.values(
                    'product__product_name',
                )
                .filter(user=request.user)
                .annotate(products=Count('product__product_name'))
                .order_by('-product__product_name')
                .distinct()[:10]
            )

            total_sum_receipts = receipts.aggregate(total=Sum('total_sum'))

            return render(
                request,
                self.template_name,
                {
                    'receipts': page_receipts,
                    'total_receipts': receipts,
                    'total_sum_receipts': total_sum_receipts,
                    'seller_form': seller_form,
                    'receipt_form': receipt_form,
                    'product_formset': product_formset,
                    'frequently_purchased_products': purchased_products,
                },
            )


class CustomerCreateView(SuccessMessageMixin, CreateView):
    model = Customer
    template_name = 'receipts/receipts.html'
    form_class = CustomerForm

    def post(self, request, *args, **kwargs):
        seller_form = CustomerForm(request.POST)
        if seller_form.is_valid():
            customer = seller_form.save(commit=False)
            customer.user = request.user
            customer.save()
            messages.success(
                self.request,
                MessageOnSite.SUCCESS_MESSAGE_CREATE_CUSTOMER.value,
            )
            response_data = {'success': True}
        else:
            response_data = {
                'success': False,
                'errors': seller_form.errors,
            }
        return JsonResponse(response_data)

    def get_success_url(self):
        return reverse_lazy('receipts:list')


class ReceiptCreateView(SuccessMessageMixin, CreateView):
    model = Receipt
    template_name = 'receipts/receipts.html'
    form_class = ReceiptForm
    success_message = MessageOnSite.SUCCESS_MESSAGE_CREATE_RECEIPT.value

    def __init__(self, *args, **kwargs):
        """
        Конструктов класса инициализирующий аргументы класса.

        :param args:
        :param kwargs:
        """
        self.request = None
        super().__init__(*args, **kwargs)

    @staticmethod
    def check_exist_receipt(request, receipt_form):
        number_receipt = receipt_form.cleaned_data.get('number_receipt')
        return Receipt.objects.filter(
            user=request.user,
            number_receipt=number_receipt,
        )

    @staticmethod
    def create_receipt(request, receipt_form, product_formset, customer):
        receipt = receipt_form.save(commit=False)
        total_sum = receipt.total_sum
        account = receipt.account
        account_balance = get_object_or_404(Account, id=account.id)
        if account_balance.user == request.user:
            account_balance.balance -= total_sum
            account_balance.save()
            receipt.user = request.user
            receipt.customer = customer
            receipt.manual = True
            receipt.save()
            for product_form in product_formset:
                product = product_form.save(commit=False)
                product.user = request.user
                product.save()
                receipt.product.add(product)
            return receipt

    def form_valid_receipt(self, receipt_form, product_formset, customer):
        number_receipt = self.check_exist_receipt(self.request, receipt_form)
        if number_receipt:
            messages.error(
                self.request,
                ReceiptConstants.RECEIPT_ALREADY_EXISTS.value,
            )
        else:
            self.create_receipt(
                self.request,
                receipt_form,
                product_formset,
                customer,
            )
            messages.success(
                self.request,
                MessageOnSite.SUCCESS_MESSAGE_CREATE_RECEIPT.value,
            )
            return {'success': True}

    def setup(self, request, *args, **kwargs):
        self.request = request
        super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_formset'] = ProductFormSet()
        return context

    def form_valid(self, form):
        customer = form.cleaned_data.get('customer')
        product_formset = ProductFormSet(self.request.POST)

        valid_form = form.is_valid() and product_formset.is_valid()
        if valid_form:
            response_data = self.form_valid_receipt(
                receipt_form=form,
                product_formset=product_formset,
                customer=customer,
            )
        else:
            response_data = {
                'success': False,
                'errors': form.errors,
            }
        return JsonResponse(response_data)

    def get_success_url(self):
        return reverse_lazy('receipts:list')


class ReceiptDeleteView(DetailView, DeleteView):
    model = Receipt
    template_name = TemplateHTMLView.RECEIPT_TEMPLATE.value
    context_object_name = 'receipts'
    no_permission_url = reverse_lazy('login')
    success_url = SuccessUrlView.RECEIPT_URL.value

    def form_valid(self, form):
        receipt = self.get_object()
        account = receipt.account
        amount = receipt.total_sum
        account_balance = get_object_or_404(Account, id=account.id)

        try:
            if account_balance.user == self.request.user:
                account_balance.balance += amount
                account_balance.save()

                for product in receipt.product.all():
                    product.delete()

                receipt.delete()
                messages.success(self.request, 'Чек успешно удалён!')
                return redirect(reverse_lazy(self.success_url))
        except ProtectedError:
            messages.error(self.request, 'Чек не может быть удалён!')
            return redirect(reverse_lazy(self.success_url))

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, ProtectedError, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView
from django_filters.views import FilterView
from hasta_la_vista_money import constants
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.commonlogic.custom_paginator import (
    paginator_custom_view,
)
from hasta_la_vista_money.commonlogic.views import collect_info_receipt
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin
from hasta_la_vista_money.receipts.forms import (
    CustomerForm,
    ProductFormSet,
    ReceiptFilter,
    ReceiptForm,
)
from hasta_la_vista_money.receipts.models import Customer, Receipt
from hasta_la_vista_money.users.models import User


class BaseView:
    template_name = 'receipts/receipts.html'
    success_url = reverse_lazy('receipts:list')


class ReceiptView(
    CustomNoPermissionMixin,
    BaseView,
    SuccessMessageMixin,
    FilterView,
):
    """Класс представления чека на сайте."""

    paginate_by = 10
    model = Receipt
    filterset_class = ReceiptFilter
    no_permission_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        user = get_object_or_404(User, username=self.request.user)
        if user.is_authenticated:
            seller_form = CustomerForm()
            receipt_filter = ReceiptFilter(
                self.request.GET,
                queryset=Receipt.objects.all(),
                user=self.request.user,
            )
            receipt_form = ReceiptForm()
            receipt_form.fields['account'].queryset = user.account_users
            receipt_form.fields[
                'customer'
            ].queryset = user.customer_users.distinct('name_seller')

            product_formset = ProductFormSet()

            list_receipts = Receipt.objects.prefetch_related('product').all()
            purchased_products = (
                list_receipts.values(
                    'product__product_name',
                )
                .filter(user=self.request.user)
                .annotate(products=Count('product__product_name'))
                .order_by('-products')
                .distinct()[:10]
            )

            total_sum_receipts = receipt_filter.qs.aggregate(
                total=Sum('total_sum'),
            )
            total_receipts = receipt_filter.qs

            receipt_info_by_month = collect_info_receipt(user=self.request.user)

            page_receipts = paginator_custom_view(
                self.request,
                total_receipts,
                self.paginate_by,
                'receipts',
            )

            # Paginator receipts table
            pages_receipt_table = paginator_custom_view(
                self.request,
                receipt_info_by_month,
                self.paginate_by,
                'receipts',
            )

            context = super().get_context_data(**kwargs)
            context['receipts'] = page_receipts
            context['receipt_filter'] = receipt_filter
            context['total_receipts'] = total_receipts
            context['total_sum_receipts'] = total_sum_receipts
            context['seller_form'] = seller_form
            context['receipt_form'] = receipt_form
            context['product_formset'] = product_formset
            context['receipt_info_by_month'] = pages_receipt_table
            context['frequently_purchased_products'] = purchased_products

            return context


class CustomerCreateView(SuccessMessageMixin, BaseView, CreateView):
    model = Customer
    form_class = CustomerForm

    def post(self, request, *args, **kwargs):
        seller_form = CustomerForm(request.POST)
        if seller_form.is_valid():
            customer = seller_form.save(commit=False)
            customer.user = request.user
            customer.save()
            messages.success(
                self.request,
                constants.SUCCESS_MESSAGE_CREATE_CUSTOMER,
            )
            response_data = {'success': True}
        else:
            response_data = {
                'success': False,
                'errors': seller_form.errors,
            }
        return JsonResponse(response_data)


class ReceiptCreateView(SuccessMessageMixin, BaseView, CreateView):
    model = Receipt
    form_class = ReceiptForm
    success_message = constants.SUCCESS_MESSAGE_CREATE_RECEIPT

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
                _(constants.RECEIPT_ALREADY_EXISTS),
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
                constants.SUCCESS_MESSAGE_CREATE_RECEIPT,
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
                'errors': product_formset.errors,
            }
        return JsonResponse(response_data)


class ReceiptDeleteView(BaseView, DetailView, DeleteView):
    model = Receipt
    context_object_name = 'receipts'

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

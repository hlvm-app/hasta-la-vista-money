from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
)
from hasta_la_vista_money.account.models import Account
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


class ReceiptView(CustomNoPermissionMixin, SuccessMessageMixin, TemplateView):
    """Класс представления чека на сайте."""

    template_name = 'receipts/receipts.html'
    model = Receipt
    context_object_name = 'receipts'
    no_permission_url = reverse_lazy('login')
    success_url = 'receipts:list'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            seller_form = CustomerForm()

            receipt_form = ReceiptForm()
            receipt_form.fields['account'].queryset = Account.objects.filter(
                user=request.user,
            )
            receipt_form.fields['customer'].queryset = Customer.objects.filter(
                user=request.user,
            ).distinct('customer')
            product_formset = ProductFormSet()
            receipts = Receipt.objects.filter(
                user=request.user,
            ).order_by('-receipt_date')

            return render(
                request,
                self.template_name,
                {
                    'receipts': receipts,
                    'seller_form': seller_form,
                    'receipt_form': receipt_form,
                    'product_formset': product_formset,
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
                'success': False, 'errors': seller_form.errors,
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
        self.request = None
        super().__init__(*args, **kwargs)

    @staticmethod
    def create_receipt(request, receipt_form, product_formset):
        receipt = receipt_form.save(commit=False)
        total_sum = receipt.total_sum
        account = receipt.account
        account_balance = get_object_or_404(Account, id=account.id)
        if account_balance.user == request.user:
            account_balance.balance -= total_sum
            account_balance.save()
            receipt.user = request.user
            receipt.save()
            for product_form in product_formset:
                product = product_form.save(commit=False)
                product.user = request.user
                product.save()
                receipt.product.add(product)
            return receipt

    @staticmethod
    def check_exist_receipt(request, receipt_form):
        number_receipt = receipt_form.cleaned_data.get('number_receipt')
        return Receipt.objects.filter(
            user=request.user, number_receipt=number_receipt,
        )

    def setup(self, request, *args, **kwargs):
        self.request = request
        super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_formset'] = ProductFormSet()
        return context

    def form_valid(self, form):
        product_formset = ProductFormSet(self.request.POST)
        response_data = {}
        valid_form = (
            form.is_valid() and
            product_formset.is_valid()
        )
        if valid_form:
            number_receipt = self.check_exist_receipt(self.request, form)
            if number_receipt:
                messages.error(
                    self.request, ReceiptConstants.RECEIPT_ALREADY_EXISTS.value,
                )
            else:
                self.create_receipt(
                    self.request,
                    form,
                    product_formset,
                )
                messages.success(
                    self.request,
                    MessageOnSite.SUCCESS_MESSAGE_CREATE_RECEIPT.value,
                )
                response_data = {'success': True}
        else:
            response_data = {
                'success': False, 'errors': form.errors,
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
                receipt.customer.delete()

                receipt.delete()
                messages.success(self.request, 'Чек успешно удалён!')
                return redirect(reverse_lazy(self.success_url))
        except ProtectedError:
            messages.error(self.request, 'Чек не может быть удалён!')
            return redirect(reverse_lazy(self.success_url))

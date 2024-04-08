import decimal
import json
import os
import tempfile

import requests
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, ProtectedError, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, FormView
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
    FileFieldForm,
    ProductFormSet,
    ReceiptFilter,
    ReceiptForm,
)
from hasta_la_vista_money.receipts.json_parser.json_parser import parse_json
from hasta_la_vista_money.receipts.models import Customer, Product, Receipt
from hasta_la_vista_money.receipts.serializers import (
    CustomerSerializer,
    ReceiptSerializer,
)
from hasta_la_vista_money.receipts.services import (
    convert_date_time,
    convert_number,
)
from hasta_la_vista_money.users.models import User
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


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
            receipt_form.fields['customer'].queryset = (
                user.customer_users.distinct('name_seller')
            )

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


class ReceiptListAPIView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = ReceiptSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Receipt.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ReceiptSerializer(queryset, many=True)
        return Response(serializer.data)


class SellerListAPIView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = ReceiptSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CustomerSerializer(queryset, many=True)
        return Response(serializer.data)


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


class CustomerCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReceiptCreateAPIView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        request_data = json.loads(request.body)
        user_id = request_data.get('user')
        account_id = request_data.get('account')
        receipt_date = request_data.get('receipt_date')
        total_sum = request_data.get('total_sum')
        number_receipt = request_data.get('number_receipt')
        operation_type = request_data.get('operation_type')
        nds10 = request_data.get('nds10')
        nds20 = request_data.get('nds20')
        customer_data = request_data.get('customer')
        products_data = request_data.get('product')

        try:
            check_existing_receipt = Receipt.objects.filter(
                receipt_date=receipt_date,
                total_sum=total_sum,
            ).first()

            if not check_existing_receipt:
                user = User.objects.get(id=user_id)
                customer_data['user'] = user
                account = Account.objects.get(id=account_id)
                account.balance -= decimal.Decimal(total_sum)
                account.save()
                request_data['account'] = account
                customer = Customer.objects.create(**customer_data)
                receipt = Receipt.objects.create(
                    user=user,
                    account=account,
                    receipt_date=receipt_date,
                    customer=customer,
                    total_sum=total_sum,
                    number_receipt=number_receipt,
                    operation_type=operation_type,
                    nds10=nds10,
                    nds20=nds20,
                )

                for product_data in products_data:
                    # Удаляем receipt из product_data, чтобы избежать ошибки
                    product_data.pop('receipt', None)
                    product_data['user'] = user
                    # Создаем продукт
                    product = Product.objects.create(**product_data)
                    # Добавляем продукт к чеку
                    receipt.product.add(product)

                return Response(
                    ReceiptSerializer(receipt).data,
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                'Такой чек уже был добавлен ранее',
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as error:
            return Response(
                str(error),
                status=status.HTTP_400_BAD_REQUEST,
            )


class ReceiptDeleteView(BaseView, DetailView, DeleteView):
    model = Receipt

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
                return redirect(self.success_url)
        except ProtectedError:
            messages.error(self.request, 'Чек не может быть удалён!')
            return redirect(self.success_url)


class FileFieldFormView(BaseView, FormView):
    form_class = FileFieldForm

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        files = form.cleaned_data['file_field']
        for file in files:
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_file = f'{tmp_dir}/{file}'
                with open(tmp_file, 'wb+') as path_tmp_file:
                    json_data = get_json_by_qrcode(self.request, path_tmp_file)
                    prepare_json(self.request, json_data)
        return super().form_valid(form=form)


def get_json_by_qrcode(request, file):
    """Получить json из сервиса API."""
    url = 'https://proverkacheka.com/api/v1/check/get'
    data = {
        'token': os.getenv('TOKEN', None),
    }
    files = {'qrfile': file}
    response = requests.post(url, data=data, files=files, timeout=10)
    json_data = response.json()
    if json_data.get('code') != 1:
        messages.error(request, json_data['data'])
        return None
    messages.success(request, 'Receipt successfully added')
    return json_data['data']['json']


def prepare_json(request, json_data):
    """Подготовить json для дальнейшей обработки."""
    if json_data:
        selected_account = parse_json(json_data, 'selected_account')
        name_seller = parse_json(json_data, 'user')
        retail_place_address = parse_json(json_data, 'retailPlaceAddress')
        retail_place = parse_json(json_data, 'retailPlace')
        items = parse_json(json_data, 'items')
        receipt_date = convert_date_time(parse_json(json_data, 'dateTime'))
        number_receipt = parse_json(json_data, 'fiscalDocumentNumber')
        nds10 = convert_number(parse_json(json_data, 'nds10'))
        nds20 = convert_number(parse_json(json_data, 'nds20'))
        total_sum = convert_number(parse_json(json_data, 'totalSum'))
        operation_type = parse_json(json_data, 'operationType')

        products = []

        for item in items:
            product_name = parse_json(item, 'product_name')

            amount = convert_number(parse_json(item, 'sum'))
            quantity = parse_json(item, 'quantity')
            price = convert_number(parse_json(item, 'price'))
            nds_type = parse_json(item, 'nds')
            nds_num = convert_number(parse_json(item, 'ndsSum'))
            products.append(
                {
                    'user': request.user.id,
                    'product_name': product_name,
                    'amount': amount,
                    'quantity': quantity,
                    'price': price,
                    'nds_type': nds_type,
                    'nds_sum': nds_num,
                },
            )

        customer = {
            'user': request.user.id,
            'name_seller': name_seller,
            'retail_place_address': retail_place_address,
            'retail_place': retail_place,
        }

        return {
            'user': request.user.id,
            'account': selected_account,
            'receipt_date': receipt_date,
            'number_receipt': number_receipt,
            'nds10': nds10,
            'nds20': nds20,
            'operation_type': operation_type,
            'total_sum': total_sum,
            'customer': customer,
            'product': products,
        }

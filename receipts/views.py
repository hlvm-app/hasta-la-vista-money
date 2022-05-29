from django.shortcuts import render
from django.utils.translation import gettext_lazy
from django.views.generic import ListView
from django_filters.views import FilterView
from django_filters import rest_framework as filters

from receipts.forms import ReceiptsFilter
from receipts.models import Receipt


class ReceiptView(FilterView):
    model = Receipt
    template_name = 'receipts/receipts.html'
    context_object_name = 'receipts'
    filterset_class = ReceiptsFilter
    filter_backends = (filters.DjangoFilterBackend,)

    error_message = gettext_lazy('У вас нет прав на просмотр данной страницы! '
                                 'Авторизуйтесь!')
    login_url = 'login'

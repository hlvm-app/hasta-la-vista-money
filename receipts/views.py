from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Subquery
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import gettext_lazy
from django.views import View
from django_filters.views import FilterView
from django_filters import rest_framework as filters

# from receipts.forms import ReceiptsFilter

from django.shortcuts import render
from .models import Customer, Receipt, Product

from django.shortcuts import render


def receipt_view(request):
    receipts = Receipt.objects.all()
    return render(request, 'receipts/receipts.html', {'receipts': receipts})









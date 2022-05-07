from django.shortcuts import render
from django.views.generic import ListView

from receipts.models import Receipts


class ReceiptView(ListView):
    model = Receipts()
    template_name = 'receipts/receipts.html'
    context_object_name = 'receipts'

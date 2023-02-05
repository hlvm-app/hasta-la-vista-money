from django.shortcuts import render, get_object_or_404

from .models import Receipt


def receipt_view(request):
    receipts = Receipt.objects.all()
    if request.method == "POST" and 'delete_button' in request.POST:
        receipt_id = request.POST.get('receipt_id')
        receipt = get_object_or_404(Receipt, pk=receipt_id)
        for product in receipt.product.all():
            product.delete()
        receipt.customer.delete()
        receipt.delete()
    return render(request, 'receipts/receipts.html', {'receipts': receipts})

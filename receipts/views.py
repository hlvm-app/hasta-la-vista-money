from django.shortcuts import render
from django.utils.translation import gettext
from django.views.generic import ListView

from receipts.models import Receipt


class ReceiptView(ListView):
    model = Receipt
    template_name = 'receipts/receipts.html'
    context_object_name = 'receipts'

    error_message = gettext('У вас нет прав на просмотр данной страницы! '
                            'Авторизуйтесь!')
    login_url = 'login'
    redirect_field_name = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('Страница с чеками')
        return context

    def get_queryset(self):
        seller = self.model.objects.all()
        return seller.model.name_seller

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



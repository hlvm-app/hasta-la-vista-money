from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin


class LoanView(CustomNoPermissionMixin, SuccessMessageMixin, TemplateView):
    template_name = 'loan/loan.html'

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from hasta_la_vista_money.constants import MessageOnSite
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin
from hasta_la_vista_money.account.models import Account


class PageApplication(CustomNoPermissionMixin, TemplateView):
    """Отображает список приложений в проекте на сайте."""

    template_name = 'applications/page_application.html'
    context_object_name = 'applications'
    permission_denied_message = MessageOnSite.ACCESS_DENIED.value
    no_permission_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        accounts = Account.objects.filter(user=request.user)
        return render(
            request,
            self.template_name,
            {'accounts': accounts},
        )

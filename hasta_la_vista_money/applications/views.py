from django.urls import reverse_lazy
from django.views.generic import TemplateView
from hasta_la_vista_money.constants import Messages
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin


class PageApplication(CustomNoPermissionMixin, TemplateView):
    """Отображает список приложений в проекте на сайте."""

    template_name = 'applications/page_application.html'
    context_object_name = 'applications'
    permission_denied_message = Messages.ACCESS_DENIED.value
    no_permission_url = reverse_lazy('login')

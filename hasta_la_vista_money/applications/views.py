from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import TemplateView

from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin


class PageApplication(CustomNoPermissionMixin, TemplateView):
    """Отображает список приложений в проекте на сайте."""

    template_name = 'applications/page_application.html'
    context_object_name = 'applications'
    permission_denied_message = gettext_lazy(
        'У вас нет прав на просмотр данной страницы! Авторизуйтесь!',
    )
    no_permission_url = reverse_lazy('users:login')

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy
from django.views.generic import ListView, TemplateView


class PageApplication(LoginRequiredMixin,
                      AccessMixin,
                      SuccessMessageMixin,
                      TemplateView):
    template_name = 'applications/page_application.html'
    context_object_name = 'applications'
    error_message = gettext_lazy('У вас нет прав на просмотр данной страницы! '
                                 'Авторизуйтесь!')
    no_permission_url = 'login'

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.no_permission_url)

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.utils.translation import gettext, gettext_lazy

from users.forms import UserAdmin


class Index(SuccessMessageMixin, LoginView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = gettext('Войти')
        context['button_register'] = gettext('Регистрация')
        return context


class IndexHastaLaVista(TemplateView):
    template_name = 'hasta_la_vista_money/index.html'
    error_message = gettext('У вас нет прав на просмотр данной страницы! '
                            'Авторизуйтесь!')
    no_permission_url = 'index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Hasta La Vista, Money :D'
        return context

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.no_permission_url)

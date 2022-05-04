from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView
from django.utils.translation import gettext, gettext_lazy

from users.forms import Admin


class Index(SuccessMessageMixin, LoginView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = gettext('Войти')
        context['button_register'] = gettext('Регистрация')
        return context


class IndexHastaLaVista(TemplateView):
    template_name = 'hasta_la_vista_money/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Hasta La Vista, Money :D'
        return context

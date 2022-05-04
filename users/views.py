from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import CreateView

from users.forms import RegisterUserForm
from users.models import Admin


class CreateUser(CreateView, SuccessMessageMixin):
    model = Admin
    template_name = 'users/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = gettext('Создать аккаунт')
        return context

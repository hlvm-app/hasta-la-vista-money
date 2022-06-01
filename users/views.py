from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy, gettext
from django.views.generic import CreateView, ListView

from users.forms import RegisterUserForm
from users.models import User


class ListUsers(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class CreateUser(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/registration.html'
    form_class = RegisterUserForm
    success_message = gettext_lazy('Регистрация прошла успешно!')
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('Форма регистрации')
        context['button_text'] = gettext('Регистрация')
        return context

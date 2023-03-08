from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView
from hasta_la_vista_money.users.forms import RegisterUserForm, UserLoginForm
from hasta_la_vista_money.users.models import User


class ListUsers(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class LoginUser(SuccessMessageMixin, LoginView):
    model = User
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_message = _('Вход успешно выполнен')
    next_page = '/applications'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = _('Войти')
        return context


class CreateUser(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/registration.html'
    form_class = RegisterUserForm
    success_message = _('Регистрация прошла успешно!')
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Форма регистрации')
        context['button_text'] = _('Регистрация')
        return context

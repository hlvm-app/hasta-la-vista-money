from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from hasta_la_vista_money.constants import MessageOnSite
from hasta_la_vista_money.users.forms import (
    RegisterUserForm,
    UpdateUserForm,
    UpdateUserPasswordForm,
    UserLoginForm,
)
from hasta_la_vista_money.users.models import User


class IndexView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('applications:list')
        return redirect('login')


class ListUsers(ListView):
    model = User
    template_name = 'header.html'
    context_object_name = 'users'


class LoginUser(SuccessMessageMixin, LoginView):
    model = User
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_message = MessageOnSite.SUCCESS_MESSAGE_LOGIN.value
    next_page = '/applications'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = _('Войти')
        return context


class LogoutUser(LogoutView, SuccessMessageMixin):

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(
            request,
            messages.SUCCESS,
            MessageOnSite.SUCCESS_MESSAGE_LOGOUT.value,
        )
        return super().dispatch(request, *args, **kwargs)


class CreateUser(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/registration.html'
    form_class = RegisterUserForm
    success_message = MessageOnSite.SUCCESS_MESSAGE_REGISTRATION.value
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Форма регистрации')
        context['button_text'] = _('Регистрация')
        return context


class UpdateUserView(SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'header.html'
    form_class = UpdateUserForm
    success_message = MessageOnSite.SUCCESS_MESSAGE_CHANGED_PROFILE.value

    def get_success_url(self):
        return reverse_lazy('applications:list')


class UpdateUserPasswordView(SuccessMessageMixin, PasswordChangeView):
    model = User
    template_name = 'header.html'
    form_class = UpdateUserPasswordForm
    success_message = MessageOnSite.SUCCESS_MESSAGE_CHANGED_PASSWORD.value

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            update_pass_user_form = UpdateUserPasswordForm(user=request.user)
            return render(
                request,
                self.template_name,
                {'update_pass_user_form': update_pass_user_form},
            )

    def get_success_url(self):
        return reverse_lazy('applications:list')

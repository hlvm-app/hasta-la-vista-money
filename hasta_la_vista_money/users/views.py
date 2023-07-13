from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, TemplateView, UpdateView
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


class ListUsers(TemplateView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_update = UpdateUserForm(instance=self.request.user)
            user_update_pass_form = UpdateUserPasswordForm(
                user=self.request.user,
            )
            context['user_update'] = user_update
            context['user_update_pass_form'] = user_update_pass_form
        return context


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
    template_name = 'users/profile.html'
    form_class = UpdateUserForm
    success_message = MessageOnSite.SUCCESS_MESSAGE_CHANGED_PROFILE.value

    def get_success_url(self):
        user = self.kwargs['pk']
        return reverse_lazy('users:profile', kwargs={'pk': user})

    def post(self, request, *args, **kwargs):
        user_update = UpdateUserForm(request.POST)
        if user_update.is_valid():
            user_update.save()
            return redirect(self.get_success_url())
        return render(
            request,
            self.template_name,
            {
                'user_update': user_update,
            },
        )


class UpdateUserPasswordView(SuccessMessageMixin, PasswordChangeView):
    model = User
    template_name = 'users/profile.html'
    form_class = UpdateUserPasswordForm
    success_message = MessageOnSite.SUCCESS_MESSAGE_CHANGED_PASSWORD.value

    def get_success_url(self):
        user = self.kwargs['pk']
        return reverse_lazy('users:profile', kwargs={'pk': user})

    def post(self, request, *args, **kwargs):
        user_update_pass_form = UpdateUserPasswordForm(request.POST)

        if user_update_pass_form.is_valid():
            user_update_pass_form.save()
            return redirect(self.get_success_url())
        return render(
            request,
            self.template_name,
            {
                'user_update_pass_form': user_update_pass_form,
            },
        )

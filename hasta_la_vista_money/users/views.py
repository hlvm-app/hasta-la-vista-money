from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, TemplateView, UpdateView
from hasta_la_vista_money.constants import MessageOnSite
from hasta_la_vista_money.custom_mixin import CustomSuccessMessageUserMixin
from hasta_la_vista_money.users.forms import (
    RegisterUserForm,
    UpdateUserForm,
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
            user_update_pass_form = PasswordChangeForm(
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


class UpdateUserView(
    CustomSuccessMessageUserMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = User
    template_name = 'users/profile.html'
    form_class = UpdateUserForm
    success_message = MessageOnSite.SUCCESS_MESSAGE_CHANGED_PROFILE.value

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance = self.request.user
        return form

    def post(self, request, *args, **kwargs):
        user_update = self.get_form()
        valid_form = (
            user_update.is_valid() and
            request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        )
        if valid_form:
            user_update.save()
            messages.success(request, self.success_message)
            response_data = {'success': True}
        else:
            response_data = {'success': False, 'errors': user_update.errors}
        return JsonResponse(response_data)


class UpdateUserPasswordView(
    CustomSuccessMessageUserMixin,
    SuccessMessageMixin,
    PasswordChangeView,
):
    model = User
    template_name = 'users/profile.html'
    form_class = PasswordChangeForm
    success_message = MessageOnSite.SUCCESS_MESSAGE_CHANGED_PASSWORD.value

    def post(self, request, *args, **kwargs):
        user_update_pass_form = PasswordChangeForm(
            data=request.POST, user=request.user,
        )
        valid_form = (
            user_update_pass_form.is_valid() and
            request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        )
        if valid_form:
            user_update_pass_form.save()
            update_session_auth_hash(request, user_update_pass_form.user)
            messages.success(request, self.success_message)
            response_data = {'success': True}
        else:
            response_data = {
                'success': False, 'errors': user_update_pass_form.errors,
            }
        return JsonResponse(response_data)

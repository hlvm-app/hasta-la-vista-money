from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, TemplateView, UpdateView
from hasta_la_vista_money import constants
from hasta_la_vista_money.commonlogic.generate_dates import generate_date_list
from hasta_la_vista_money.custom_mixin import (
    CustomNoPermissionMixin,
    CustomSuccessURLUserMixin,
)
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


class ListUsers(CustomNoPermissionMixin, SuccessMessageMixin, TemplateView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'users'
    no_permission_url = reverse_lazy('login')

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
    success_message = constants.SUCCESS_MESSAGE_LOGIN
    next_page = '/hasta-la-vista-money'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = _('Войти')
        context['user_login_form'] = UserLoginForm()
        return context

    def form_invalid(self, form):
        messages.error(
            self.request,
            form.errors['__all__'][0],
        )
        return super().form_invalid(form)


class LogoutUser(LogoutView, SuccessMessageMixin):
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(
            request,
            messages.SUCCESS,
            constants.SUCCESS_MESSAGE_LOGOUT,
        )
        return super().dispatch(request, *args, **kwargs)


class CreateUser(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/registration.html'
    form_class = RegisterUserForm
    success_message = constants.SUCCESS_MESSAGE_REGISTRATION
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if User.objects.filter(is_superuser=True).exists():
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Форма регистрации')
        context['button_text'] = _('Регистрация')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.is_superuser = True
        self.object.is_staff = True
        self.object.save()
        date_time_user_registration = self.object.date_joined
        generate_date_list(date_time_user_registration, self.object)
        return response


class UpdateUserView(
    CustomSuccessURLUserMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = User
    template_name = 'users/profile.html'
    form_class = UpdateUserForm
    success_message = constants.SUCCESS_MESSAGE_CHANGED_PROFILE

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance = self.request.user
        return form

    def post(self, request, *args, **kwargs):
        user_update = self.get_form()
        valid_form = (
            user_update.is_valid()
            and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        )
        if valid_form:
            user_update.save()
            messages.success(request, self.success_message)
            response_data = {'success': True}
        else:
            response_data = {'success': False, 'errors': user_update.errors}
        return JsonResponse(response_data)

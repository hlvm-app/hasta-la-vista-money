from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, TemplateView, UpdateView
from hasta_la_vista_money.bot.send_message.send_message_tg_user import (
    SendMessageToTelegramUser,
)
from hasta_la_vista_money.constants import MessageOnSite, TemplateHTMLView
from hasta_la_vista_money.custom_mixin import (
    CustomNoPermissionMixin,
    CustomSuccessURLUserMixin,
)
from hasta_la_vista_money.users.forms import (
    ForgotPasswordForm,
    RegisterUserForm,
    UpdateUserForm,
    UserLoginForm,
)
from hasta_la_vista_money.users.models import TelegramUser, User


class IndexView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('applications:list')
        return redirect('login')


class ListUsers(CustomNoPermissionMixin, SuccessMessageMixin, TemplateView):
    model = User
    template_name = TemplateHTMLView.USERS_TEMPLATE_PROFILE.value
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
    success_message = MessageOnSite.SUCCESS_MESSAGE_LOGIN.value
    next_page = '/hasta-la-vista-money'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = _('Войти')
        context['user_login_form'] = UserLoginForm()
        context['reset_password_form'] = ForgotPasswordForm()
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
    CustomSuccessURLUserMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = User
    template_name = TemplateHTMLView.USERS_TEMPLATE_PROFILE.value
    form_class = UpdateUserForm
    success_message = MessageOnSite.SUCCESS_MESSAGE_CHANGED_PROFILE.value

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


class UpdateUserPasswordView(
    CustomSuccessURLUserMixin,
    SuccessMessageMixin,
    PasswordChangeView,
):
    model = User
    template_name = TemplateHTMLView.USERS_TEMPLATE_PROFILE.value
    form_class = PasswordChangeForm
    success_message = MessageOnSite.SUCCESS_MESSAGE_CHANGED_PASSWORD.value

    def post(self, request, *args, **kwargs):
        user_update_pass_form = PasswordChangeForm(
            data=request.POST,
            user=request.user,
        )
        valid_form = (
            user_update_pass_form.is_valid()
            and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        )
        if valid_form:
            user_update_pass_form.save()
            update_session_auth_hash(request, user_update_pass_form.user)
            messages.success(request, self.success_message)
            response_data = {'success': True}
        else:
            response_data = {
                'success': False,
                'errors': user_update_pass_form.errors,
            }
        return JsonResponse(response_data)


class ForgotPasswordView(
    SuccessMessageMixin,
    TemplateView,
):
    form_class = ForgotPasswordForm
    template_name = 'users/login.html'
    success_url = 'https://t.me/GetReceiptBot'

    def get(self, request, *args, **kwargs):
        reset_password_form = ForgotPasswordForm()
        return render(
            request,
            self.template_name,
            {'reset_password_form': reset_password_form},
        )

    def post(self, request, *args, **kwargs):
        reset_password_form = ForgotPasswordForm(request.POST)
        if reset_password_form.is_valid():
            username = reset_password_form.cleaned_data.get('username')
            user = User.objects.filter(username=username).first()
            telegram_user = TelegramUser.objects.filter(user=user).first()
            if telegram_user:
                token = default_token_generator.make_token(user)
                current_site = get_current_site(request)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = ''.join(
                    (
                        f'https://{current_site.domain}',
                        f"{reverse_lazy('users:custom-password-reset-confirm', args=[uid, token])}",  # noqa: E501
                    ),
                )
                message = ''.join(
                    (
                        f'Привет, {telegram_user.username}!\n',
                        'Кто-то запросил сброс пароля ',
                        'для вашей учетной записи.\n',
                        'Ссылка действует сутки.\n',
                        'Если это были не вы, просто удалите сообщение.\n',
                        f'Для сброса пароля перейдите по ссылке: {reset_link}',
                    ),
                )
                SendMessageToTelegramUser.send_message_to_telegram_user(
                    telegram_user.telegram_id,
                    message,
                )
                return redirect(self.success_url)
        return render(
            request,
            self.template_name,
            {'reset_password_form': reset_password_form},
        )


class CustomPasswordResetConfirmView(
    SuccessMessageMixin,
    PasswordResetConfirmView,
):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Пароль успешно изменён!')
        return redirect(self.success_url)

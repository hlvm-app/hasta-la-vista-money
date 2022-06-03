from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView
from django.utils.translation import gettext, gettext_lazy

from users.forms import User, UserLoginForm


class LoginUser(SuccessMessageMixin, LoginView):
    model = User
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_message = gettext_lazy('Вход успешно выполнен')
    next_page = reverse_lazy('applications')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = gettext('Войти')
        return context


# class PageApplication(LoginRequiredMixin,
#                       ListView,
#                       SuccessMessageMixin,
#                       AccessMixin):
#
#     template_name = 'hasta_la_vista_money/page_application.html'
#     error_message = gettext('У вас нет прав на просмотр данной страницы! '
#                             'Авторизуйтесь!')
#     no_permission_url = 'login'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = gettext('Страница приложений')
#         return context
#
#     def handle_no_permission(self):
#         messages.error(self.request, self.error_message)
#         return redirect(self.no_permission_url)

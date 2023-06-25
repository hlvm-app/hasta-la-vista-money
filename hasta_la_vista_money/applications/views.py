from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from hasta_la_vista_money.account.forms import AddAccountForm
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.buttons_delete import button_delete_account
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin


class PageApplication(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    TemplateView,
):
    """Отображает список приложений в проекте на сайте."""

    model = Account
    template_name = 'applications/page_application.html'
    context_object_name = 'applications'
    no_permission_url = reverse_lazy('login')
    success_url = 'applications:list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            accounts = Account.objects.filter(user=self.request.user)
            context['accounts'] = accounts
            context['add_account_form'] = AddAccountForm()
        return context

    def post(self, request, *args, **kwargs):
        if 'delete_account_button' in request.POST:
            account_id = request.POST.get('account_id')
            button_delete_account(
                Account,
                request,
                account_id,
                self.success_url,
            )

        account_form = AddAccountForm(request.POST)
        if account_form.is_valid():
            add_account = account_form.save(commit=False)
            if request.user:
                add_account.user = request.user
                add_account.save()
                return redirect(reverse_lazy(self.success_url))
        else:
            return self.render_to_response(
                {
                    'add_account_form': account_form,
                },
            )

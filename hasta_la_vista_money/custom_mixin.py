from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from hasta_la_vista_money.constants import MessageOnSite


class CustomNoPermissionMixin(LoginRequiredMixin):
    no_permission_url = None
    permission_denied_message = ''
    redirect_field_name = ''
    request = ''

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.no_permission_url)


class DeleteCategoryMixin(DeleteView):
    model = None
    success_url = None

    def form_valid(self, form):
        try:
            category = self.object
            category.delete()
            messages.success(
                self.request, MessageOnSite.SUCCESS_CATEGORY_DELETED.value,
            )
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request, MessageOnSite.ACCESS_DENIED_DELETE_CATEGORY.value,
            )
            return redirect(self.success_url)


class CustomSuccessURLUserMixin:
    def __init__(self):
        self.kwargs = None

    def get_success_url(self):
        user = self.kwargs['pk']
        return reverse_lazy('users:profile', kwargs={'pk': user})


class ExpenseIncomeFormValidCreateMixin(CreateView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = None

    def form_valid(self, form):
        category_form = form.save(commit=False)
        category_form.user = self.request.user
        category_form.save()
        messages.success(
            self.request, MessageOnSite.SUCCESS_CATEGORY_ADDED.value,
        )
        return super().form_valid(form)

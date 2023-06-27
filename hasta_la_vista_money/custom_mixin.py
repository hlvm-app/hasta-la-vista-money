from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DeleteView, DetailView


class CustomNoPermissionMixin(LoginRequiredMixin):
    no_permission_url = None
    permission_denied_message = ''
    redirect_field_name = ''
    request = ''

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.no_permission_url)


class DeleteCategoryMixin(DetailView, DeleteView):
    success_url = None

    def form_valid(self, form):
        success = self.delete_category()
        if success:
            success_message = self.get_success_message()
            if success_message:
                messages.success(self.request, success_message)
            return super().form_valid(form)
        error_message = self.get_error_message()
        messages.error(self.request, error_message)
        return redirect(self.get_success_url())

    def get_error_message(self):
        return ''

    def get_success_message(self):
        return ''

    def delete_category(self):
        raise NotImplementedError('Subclasses must implement delete_category()')

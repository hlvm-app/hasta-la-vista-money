from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class CustomNoPermissionMixin(LoginRequiredMixin):
    no_permission_url = None
    permission_denied_message = ''
    redirect_field_name = ''
    request = ''

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.no_permission_url)

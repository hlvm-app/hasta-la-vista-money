from django.shortcuts import redirect
from django.urls import reverse_lazy
from hasta_la_vista_money.users.models import User


class CheckAdminMiddleware:
    def __init__(self, get_response):
        """init."""
        self.get_response = get_response

    def __call__(self, request):
        if not User.objects.filter(is_superuser=True).exists():
            if request.path != reverse_lazy('users:registration'):
                return redirect('users:registration')
        return self.get_response(request)

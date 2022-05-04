from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic import FormView

from users.models import Admin


class UserLogin(FormView):
    class Meta:
        model = Admin
        fields = [
            'username',
            'password',
        ]


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = Admin
        fields = ['first_name', 'last_name', 'username', 'password1',
                  'password2']

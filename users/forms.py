from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView

from users.models import User


class UserLogin(FormView):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1',
                  'password2']

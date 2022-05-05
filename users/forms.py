from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic import FormView

from users.models import UserAdmin


class UserLogin(FormView):
    class Meta:
        model = UserAdmin
        fields = [
            'username',
            'password',
        ]


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = UserAdmin
        fields = ['first_name', 'last_name', 'username', 'password1',
                  'password2']

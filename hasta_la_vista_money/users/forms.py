from django.contrib.auth.forms import (
    AuthenticationForm,
    ReadOnlyPasswordHashField,
    SetPasswordForm,
    UserChangeForm,
    UserCreationForm,
)
from hasta_la_vista_money.constants import MessageOnSite
from hasta_la_vista_money.users.models import User


class UserLoginForm(AuthenticationForm):
    username = User.username
    password = User.password
    fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'password1', 'password2',
        ]


class UpdateUserForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label='',
        help_text=MessageOnSite.SUCCESS_MESSAGE_SET_PASSWORD.value,
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username',
        ]


class UpdateUserPasswordForm(SetPasswordForm):
    class Meta:
        model = User

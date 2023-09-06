from django.contrib.auth.forms import (
    AuthenticationForm,
    ReadOnlyPasswordHashField,
    UserCreationForm,
)
from django.forms import CharField, ModelForm, forms
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
            'username',
            'password1',
            'password2',
        ]


class ForgotPasswordForm(forms.Form):
    username = CharField(
        label='Имя пользователя',
        help_text=MessageOnSite.HELP_TEXT_FORGOT_PASSWORD.value,
    )


class UpdateUserForm(ModelForm):
    password = ReadOnlyPasswordHashField(
        label='',
        help_text=MessageOnSite.HELP_TEXT_PASSWORD.value,
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
        ]

from django.contrib.auth.forms import (
    AuthenticationForm,
    ReadOnlyPasswordHashField,
    UserCreationForm,
)
from django.forms import CharField, ModelForm, forms
from hasta_la_vista_money import constants
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
        help_text=constants.HELP_TEXT_FORGOT_PASSWORD,
    )


class UpdateUserForm(ModelForm):
    password = ReadOnlyPasswordHashField(
        label='',
        help_text=constants.HELP_TEXT_PASSWORD,
    )

    class Meta:
        model = User
        fields = [
            'username',
        ]

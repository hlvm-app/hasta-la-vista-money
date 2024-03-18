from django.contrib.auth.forms import (
    AuthenticationForm,
    ReadOnlyPasswordHashField,
    UserCreationForm,
)
from django.forms import CharField, ModelForm, forms
from hasta_la_vista_money import constants
from hasta_la_vista_money.users.models import CustomUser


class UserLoginForm(AuthenticationForm):
    username = CustomUser.username
    password = CustomUser.password
    fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
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
        model = CustomUser
        fields = [
            'username',
        ]

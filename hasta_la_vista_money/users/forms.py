from django.contrib.auth.forms import (
    AuthenticationForm,
    ReadOnlyPasswordHashField,
    UserCreationForm,
)
from django.forms import BooleanField, CharField, ModelForm, forms
from hasta_la_vista_money.constants import MessageOnSite
from hasta_la_vista_money.users.models import User


class UserLoginForm(AuthenticationForm):
    username = User.username
    password = User.password
    fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    policy = BooleanField(label='Политика конфиденциальности', required=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'policy',
            'username',
            'password1',
            'password2',
        ]


class ForgetPasswordForm(forms.Form):
    username = CharField(label='Имя пользователя')


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

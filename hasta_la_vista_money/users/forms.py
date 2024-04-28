from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
    AuthenticationForm,
    ReadOnlyPasswordHashField,
    UserCreationForm,
)
from django.forms import CharField, ModelForm, PasswordInput, ValidationError
from hasta_la_vista_money import constants
from hasta_la_vista_money.commonlogic.check_user import check_user
from hasta_la_vista_money.users.models import User


class UserLoginForm(AuthenticationForm):
    username = CharField(
        max_length=constants.TWO_HUNDRED_FIFTY,
        label='Имя пользователя или Email',
    )
    password = CharField(
        label='Пароль',
        strip=False,
        widget=PasswordInput,
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = check_user(username)
        if user and user.check_password(password):
            self.user_cache = authenticate(
                request=self.request,
                username=user.username,
                password=password,
            )
            if self.user_cache is None:
                raise ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )

        return self.cleaned_data


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


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

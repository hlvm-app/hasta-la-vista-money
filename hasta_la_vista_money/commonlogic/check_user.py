from hasta_la_vista_money.users.models import User


def check_user(username):
    """Функция проверка существования пользователя в базе данных."""
    try:
        if '@' in username:
            user = User.objects.get(email=username)
        else:
            user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    return user

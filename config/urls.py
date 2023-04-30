from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from hasta_la_vista_money.users.views import LoginUser

urlpatterns = [
    re_path(
        'users/',
        include(
            'hasta_la_vista_money.users.urls',
            namespace='users',
        ),
        name='list',
    ),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path(
        'login/',
        LoginUser.as_view(
            redirect_authenticated_user=True,
        ),
        name='login',
    ),
    path(
        'applications/',
        include(
            'hasta_la_vista_money.applications.urls', namespace='applications',
        ),
        name='applications',
    ),
    path(
        'receipts/',
        include(
            'hasta_la_vista_money.receipts.urls',
            namespace='receipts',
        ),
        name='receipt',
    ),
    path(
        'income/',
        include(
            'hasta_la_vista_money.income.urls',
            namespace='income',
        ),
        name='income',
    ),
    path(
        'expense/',
        include(
            'hasta_la_vista_money.expense.urls',
            namespace='expense',
        ),
        name='expense',
    ),
    path(
        'bot/',
        include(
            'hasta_la_vista_money.bot.urls', namespace='bot',
        ),
        name='bot',
    ),
    path('adminushka/', admin.site.urls),
]

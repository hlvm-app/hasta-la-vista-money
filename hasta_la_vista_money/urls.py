"""hasta_la_vista_money URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from hasta_la_vista_money.users.views import LoginUser


urlpatterns = [
    re_path(r'users/',
            include('hasta_la_vista_money.users.urls', namespace='users'),
            name='list'),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('login/', LoginUser.as_view(redirect_authenticated_user=True),
         name='login'),
    path('applications/', include('hasta_la_vista_money.applications.urls',
                                  namespace='applications'),
         name='applications'),
    path('receipts/', include('hasta_la_vista_money.receipts.urls',
                              namespace='receipts'), name='receipt'),
    path('income/', include('hasta_la_vista_money.income.urls',
                            namespace='income'), name='income'),
    path('expense/', include('hasta_la_vista_money.expense.urls',
                             namespace='expense'), name='expense'),
    path('adminushka/', admin.site.urls),
]

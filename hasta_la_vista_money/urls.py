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
# from django.contrib import admin
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from hasta_la_vista_money.views import LoginUser, PageApplication
from receipts.views import ReceiptView

urlpatterns = [
    re_path(r'users/',
            include('users.urls', namespace='users'), name='list'),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('login/', LoginUser.as_view(redirect_authenticated_user=True),
         name='login'),
    path('applications/', PageApplication.as_view(), name='applications'),
    path('receipts/', ReceiptView.as_view(), name='receipts'),
    path('adminushka/', admin.site.urls),
]

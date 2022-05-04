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
from django.urls import path

from hasta_la_vista_money.views import Index, IndexHastaLaVista
from users.views import CreateUser

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('registration/', CreateUser.as_view(), name='register'),
    path('hastalavistamoney/', IndexHastaLaVista.as_view(),
         name='hastalavista'),
    path('adminushka/', admin.site.urls),
]

from django.urls import path

from applications.views import PageApplication


app_name = 'applications'
urlpatterns = [
    path('', PageApplication.as_view(), name='list')
]

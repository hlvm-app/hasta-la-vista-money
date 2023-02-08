from django.urls import path

from hasta_la_vista_money.applications.views import PageApplication

app_name = 'applications'
urlpatterns = [
    path('', PageApplication.as_view(), name='list'),

]

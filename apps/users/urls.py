from django.urls import path

from apps.users.views import *
urlpatterns = [
    path('', users, name='users')
]

from django.urls import path

from apps.home.views import *
urlpatterns = [
    path('', home, name='home')
]

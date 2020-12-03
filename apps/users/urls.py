from django.urls import path

from apps.users.views import *
urlpatterns = [
    path('', users, name='users'),
    #show user with user_id
    path('show/<str:user_id>', show, name='show'),
    #Show all users
    path('show_all', show_all, name='show_all'),
    #Create user
    path('create/<str:new_user>', create, name='create'),
    #Delete user
    path('delete/<str:user2delete>', delete, name='delete'),
    # Modify user
    path('modify/<str:user2modify>', modify, name='modify'),
]

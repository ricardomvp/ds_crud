from django.urls import path

from apps.teams.views import *
urlpatterns = [
    path('', teams, name='teams'),
    #show team with team_is
    path('show/<str:team_id>', show, name='show'),
    #Show all teams
    path('show_all', show_all, name='show_all'),

    #Add new teamamte to team
    path('add/<str:teammate>', add, name='new_teammate'),
    #Remove teammate from team
    path('remove/<str:teammate>', remove, name='remove'),

    #Create team
    path('create/<str:teamname>', create, name='create'),
    #Delete team
    path('delete/<str:teamname>', delete, name='delete'),
    # Modify team
    path('modify/<str:teamname>', modify, name='modify'),
]

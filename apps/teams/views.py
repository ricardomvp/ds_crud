#standard libraries
import json
import base64
#Django libraries
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.core import serializers
from django.conf import settings
#Get models
from apps.teams.models import Team, Member
from apps.users.models import User,Profile
#Utils
from utils.utils import _add_users_to_team, _new_team_email, _get_admins

def teams(request):
    data = {'data' : 'you are in Teams page'}
    return JsonResponse(data)

#Show only the team with team_id
def show(request, team_id):
    team_id = int(team_id)
    team = Team.objects.filter(id=team_id)
    data = _add_users_to_team(team)
    if not data:
        data={'request':'Team is Not found'}
    return JsonResponse(data, safe=False)

#Show all teams
def show_all(request):
    teams = Team.objects.all()
    data = _add_users_to_team(teams)
    return JsonResponse(data, safe=False)

"""
Add new teammate to team
request -> {"user" : "USER_NAME","team" : "TEAM_NAME"}
"""
def add(request):
    if request.method == 'POST':
        #Get user
        try:
            user = User.objects.get(name=request.POST['user'])
            user = Profile.objects.get(user=user)
        except:
            data={'data' : 'Username not found'}
            return JsonResponse(data)
        # Get team
        try:
            team = Team.objects.get(name=request.POST['team'])
        except:
            data={'data' : 'Team name not found'}
            return JsonResponse(data)
        #Add user to team
        new_member = Member.objects.create()
        new_member.team = team
        new_member.user = user
        new_member.save()
        return redirect(f'/teams/show/{team.id}')

"""
Remove teammate from existent team
request -> {"user" : "USER_NAME","team" : "TEAM_NAME"}
"""
def remove(request):
    if request.method == 'POST':
        #Get user
        try:
            user = User.objects.get(name=request.POST['user'])
            user = Profile.objects.get(user=user)
        except:
            data={'data' : 'Username not found'}
            return JsonResponse(data)
        # Get team
        try:
            team = Team.objects.get(name=request.POST['team'])
        except:
            data={'data' : 'Team name not found'}
            return JsonResponse(data)
        #Remove user from team
        Member = Member.objects.filter(team=team).get(user=user)
        Member.delete()
        return redirect(f'/teams/show/{team.id}')

"""
Create new team
request -> {"name" : "NEW_TEAM_NAME"}
"""
def create(request):
    current_user = request.user
    if request.method == 'POST':
        #Create new Team
        new_team = Team.objects.create()
        #Set name
        new_team.name = request.POST['name']
        #Get curren user
        user = Profile.objects.get(user=current_user)
        #set current user as creator
        new_team.created_by = user
        new_team.modified_by = user
        #save
        new_team.save()
        #Add current user to new team
        new_member = Member.objects.create()
        new_member.team = new_team
        new_member.user = user
        new_member.save()
        #Send New Team Email
        subject = 'New Team was created'
        message = f'A new team "{new_team.name}" was created by {user.user.name} ({user.user.email}). See it on http://127.0.0.1:8000/admin/teams/team/{new_team.pk}/change/'
        email_to = ['ricardom.ipn@gmail.com']
        # Get admins
        # admins = _get_admins() ##Pass
        # email_to =admins
        _new_team_email(subject, message, email_to)

        return redirect(f'/teams/show/{new_team.id}')

"""
Delete team
request -> {"name" : "TEAM_NAME_2_DELETE"}
"""
def delete(request):
    if request.method == 'POST':
        #Disable team
        try:
            team = Team.objects.get(name=request.POST['name'])
        except:
            data={'data' : 'Teamname not found'}
            return JsonResponse(data)
        if team.active == False:
             data={'data' : 'Team was deleted previosly'}
             return JsonResponse(data)
        team.active = False
        team.save()
        return redirect(f'/teams/show/{team.id}')

"""
Modify team
request -> {"name" : "TEAM_NAME_2_MODIFY",
              "new_name":"NEW_NAME",
              "local_image":"NEW_IMAGE",
              }
"""
def modify(request):
    if request.method == 'POST':
        #Disable team
        try:
            team = Team.objects.get(name=request.POST['name'])
        except:
            data={'data' : 'Teamname not found'}
            return JsonResponse(data)
        if team.active == False:
            data={'data' : 'Team is deleted'}
            return JsonResponse(data)
        #set modifications if they exist
        if 'new_name' in request.POST:
            team.name = request.POST['new_name']
        if 'local_image' in request.POST:
            path = request.POST['local_image']
            _, name_file = path.split('/')[-1]
            with open (path, "rb") as img_file:
                data = base64.b64encode(img_file.read())
            team.image.save(name, ContentFile(data))
        team.save()
        return redirect(f'/teams/show/{team.id}')

#standard libraries
import json
#Django libraries
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.core import serializers
from django.conf import settings
#Get models
from apps.teams.models import Team, Member
from apps.users.models import User,Profile
#Utils
from utils.utils import _add_users_to_team

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
structure -> {"user" : "USER_NAME","team" : "TEAM_NAME"}
"""
def add(request, teammate):
    #Check if dict has a correct structure
    try:
        teammate = json.loads(teammate)
    except:
        data = {'request' :'Bad Query'}
        return JsonResponse(data)
    #Check if dict has all required elements
    required_field=['user', 'team']
    for field in required_field:
        if not field in teammate:
            data ={'data' : f'{field} field must be added in request'}
            return JsonResponse(data, safe=False)

    #Get user
    try:
        user = User.objects.get(name=teammate['user'])
        user = Profile.objects.get(user=user)
    except:
        data={'data' : 'Username not found'}
        return JsonResponse(data)
    # Get team
    try:
        team = Team.objects.get(name=teammate['team'])
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
structure -> {"user" : "USER_NAME","team" : "TEAM_NAME"}
"""
def remove(request, teammate):
    #Check if dict has a correct structure
    try:
        teammate = json.loads(teammate)
    except:
        data = {'request' :'Bad Query'}
        return JsonResponse(data)
    #Check if dict has all required elements
    required_field=['user', 'team']
    for field in required_field:
        if not field in teammate:
            data ={'data' : f'{field} field must be added in request'}
            return JsonResponse(data, safe=False)
    #Get user
    try:
        user = User.objects.get(name=teammate['user'])
        user = Profile.objects.get(user=user)
    except:
        data={'data' : 'Username not found'}
        return JsonResponse(data)
    # Get team
    try:
        team = Team.objects.get(name=teammate['team'])
    except:
        data={'data' : 'Team name not found'}
        return JsonResponse(data)
    #Remove user from team
    Member = Member.objects.filter(team=team).get(user=user)
    Member.delete()
    return redirect(f'/teams/show/{team.id}')

"""
Create new team
structure -> {"name" : "NEW_TEAM_NAME"}
"""
def create(request, teamname):
    current_user = request.user
    #Check if dict has a correct structure
    try:
        teamname = json.loads(teamname)
    except:
        data = {'request' :'Bad Query'}
        return JsonResponse(data)
    #Check if dict has all required elements
    required_field=['name']
    for field in required_field:
        if not field in teamname:
            data ={'data' : f'{field} field must be added in request'}
            return JsonResponse(data, safe=False)

    #Create new Team
    new_team = Team.objects.create()
    #Set name
    new_team.name = teamname['name']
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

    _new_team_email(user, new_team)


    return redirect(f'/teams/show/{new_team.id}')

"""
Delete team
structure -> {"name" : "TEAM_NAME_2_DELETE"}
"""
def delete(request, teamname):
    #Check if dict has a correct structure
    try:
        teamname = json.loads(teamname)
    except:
        data = {'request' :'Bad Query'}
        return JsonResponse(data)
    #Check if dict has all required elements
    required_field=['name']
    for field in required_field:
        if not field in teamname:
            data ={'data' : f'{field} field must be added in request'}
            return JsonResponse(data, safe=False)
    #Disable team
    try:
        team = Team.objects.get(name=teamname['name'])
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
structure -> {"name" : "TEAM_NAME_2_MODIFY",
              "new_name":"NEW_NAME",
              "new_image":"NEW_IMAGE",
              }
"""
def modify(request, teamname):
    #Check if dict has a correct structure
    try:
        teamname = json.loads(teamname)
    except:
        data = {'request' :'Bad Query'}
        return JsonResponse(data)
    #Check if dict has all required elements
    required_field=['name']
    for field in required_field:
        if not field in teamname:
            data ={'data' : f'{field} field must be added in request'}
            return JsonResponse(data, safe=False)
    #Disable team
    try:
        team = Team.objects.get(name=teamname['name'])
    except:
        data={'data' : 'Teamname not found'}
        return JsonResponse(data)
    if team.active == False:
        data={'data' : 'Team is deleted'}
        return JsonResponse(data)
    #set modifications if they exist
    if 'new_name' in teamname:
        team.name = teamname['new_name']
    # if 'new_image' in teamname:
    #     team.image = teamname['new_image']
    team.save()
    return redirect(f'/teams/show/{team.id}')


def _new_team_email(user, new_team):
    #send recovering email
    subject = 'New Team was created'
    message = f'A new team {new_team.name} was created by {user.user.name} ({user.user.email}).'
    email_from = settings.EMAIL_HOST_USER
    email_to = ['ricardom.ipn@gmail.com']
    send_mail(subject, message, email_from, email_to, fail_silently=False,)

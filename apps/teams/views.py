#standard libraries
import json
#Django libraries
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.shortcuts import redirect
#Get apps
from apps.teams.models import Team, UserTeam
from apps.users.models import User,TeamMate

def teams(request):
    data = {'data' : 'you are in Teams page'}
    return JsonResponse(data)

#Show only the team with team_id
def show(request, team_id):
    team_id = int(team_id)
    team = Team.objects.filter(id=team_id)
    data = _get_request(team)
    if not data:
        data={'request':'Team id Not found'}
    return JsonResponse(data, safe=False)

#Show all teams
def show_all(request):
    teams = Team.objects.all()
    data = _get_request(teams)
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
        return JsonResponse(data, safe=False)
    #Check if dict has user & team in its context
    if not 'user' in teammate:
        data ={'data' : 'user field must be added in request'}
        return JsonResponse(data, safe=False)
    if not 'team' in teammate:
        data ={'data' : 'team field must be added in request'}
        return JsonResponse(data, safe=False)
    #Get user
    try:
        user = User.objects.get(name=teammate['user'])
        user = TeamMate.objects.get(user=user)
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
    new_userteam = UserTeam.objects.create()
    new_userteam.team = team
    new_userteam.user = user
    new_userteam.save()
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
        return JsonResponse(data, safe=False)
    #Check if dict has user & team in its context
    if not 'user' in teammate:
        data ={'data' : 'user field must be added in request'}
        return JsonResponse(data, safe=False)
    if not 'team' in teammate:
        data ={'data' : 'team field must be added in request'}
        return JsonResponse(data, safe=False)
    #Get user
    try:
        user = User.objects.get(name=teammate['user'])
        user = TeamMate.objects.get(user=user)
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
    userteam = UserTeam.objects.filter(team=team).get(user=user)
    userteam.delete()
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
        return JsonResponse(data, safe=False)
    #Check if dict has name in its contect
    if not 'name' in teamname:
        data ={'data' : 'name field must be added in request'}
        return JsonResponse(data, safe=False)
    #Create new Team
    new_team = Team.objects.create()
    #Set name
    new_team.name = teamname['name']
    #Get curren user
    user = TeamMate.objects.get(user=current_user)
    #set current user as creator
    new_team.created_by = user
    new_team.modified_by = user
    #save
    new_team.save()
    #Add current user to new team
    new_userteam = UserTeam.objects.create()
    new_userteam.team = new_team
    new_userteam.user = user
    new_userteam.save()
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
        return JsonResponse(data, safe=False)
    #Check if dict has name in its contect
    if not 'name' in teamname:
        data ={'data' : 'name field must be added in request'}
        return JsonResponse(data, safe=False)
    #Disable team
    try:
        team = Team.objects.get(name=teamname['name'])
    except:
        data={'data' : 'Teamname not found'}
        return JsonResponse(data)
    team.active = False
    team.save()

    return redirect(f'/teams/show/{team.id}')

"""
Modify team
structure -> {"name" : "TEAM_NAME_2_MODIFY", "new_name":"NEW_NAME", "new_image":"NEW_IMAGE"}
"""
def modify(request, teamname):
    #Check if dict has a correct structure
    try:
        teamname = json.loads(teamname)
    except:
        data = {'request' :'Bad Query'}
        return JsonResponse(data, safe=False)
    #Check if dict has name in its contect
    if not 'name' in teamname:
        data ={'data' : 'name field must be added in request'}
        return JsonResponse(data, safe=False)
    #Disable team
    try:
        team = Team.objects.get(name=teamname['name'])
    except:
        data={'data' : 'Teamname not found'}
        return JsonResponse(data)

    if 'new_name' in teamname:
        team.name = teamname['new_name']
    # if 'new_image' in teamname:
    #     team.image = teamname['new_image']

    team.save()

    return redirect(f'/teams/show/{team.id}')


"""
Given a team(s) object(s), return the same dict but with all
its teamates in the key ['teamates']
"""
def _get_request(teams):
    team_request = json.loads(serializers.serialize('json',teams))
    usersteam = UserTeam.objects.all()
    usersteam_request = json.loads(serializers.serialize('json',usersteam))
    request=[]
    for team in team_request:
        temp={}
        for user in usersteam_request:
            if team['pk']==user['fields']['team']:
                temp[user['fields']['user']] = TeamMate.objects.get(id=user['fields']['user']).user.name
        team['teammates'] = temp
        request.append(team)
    return request

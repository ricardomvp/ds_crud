#standard libraries
import json
#django libraries
from django.core import serializers
from django.core.mail import send_mail
from django.conf import settings
#Get models
from apps.teams.models import  Team, Member
from apps.users.models import User, Profile

"""
Given a team(s) object(s), return the same dict but with all
its teamates in the key ['teamates']
"""
def _add_users_to_team(teams):
    team_request = json.loads(serializers.serialize('json',teams))
    usersteam = Member.objects.all()
    usersteam_request = json.loads(serializers.serialize('json',usersteam))
    request=[]
    for team in team_request:
        temp={}
        for user in usersteam_request:
            if team['pk']==user['fields']['team']:
                #Get filters
                name = Profile.objects.get(id=user['fields']['user'])
                get_team = Team.objects.get(name=team['fields']['name'])
                #Append team members
                temp[user['fields']['user']] = {
                                                'name': name.user.name,
                                                'joined' : Member.objects.filter(team=get_team).get(user=name).join_date
                                                }
        team['teammates'] = temp
        request.append(team)
    return request


"""
Send email related to teams
"""
def _new_team_email(subject, message, email_to):
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, email_to, fail_silently=False,)

"""
Get admins from profiles
"""
def _get_admins():
    #Get admins
    profiles = Profile.objects.filter(is_admin=True)
    admins=[]
    #Make a list with admins email
    for profile in profiles:
        admins.append(profile.user.email)
    return admins

"""
Check Teams availability
"""
def _check_teams_availability():
    teams = Teams.objects.all()
    for team in teams:
        members = Members.objects.filter(team=team).count()
        if members >= 10:
            #Send New Team Email
            subject = 'Team has exceed availability'
            message = f'Warning! Team {team.name} has {members} members.'
            email_to = ['ricardom.ipn@gmail.com']
            # Get admins
            # admins = _get_admins() ##Pass
            # email_to =admins
            _new_team_email(subject, message, email_to)

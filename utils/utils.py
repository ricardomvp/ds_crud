#standard libraries
import json
#django libraries
from django.core import serializers
#Get models
from apps.teams.models import  Member
from apps.users.models import Profile

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
                temp[user['fields']['user']] = Profile.objects.get(id=user['fields']['user']).user.name
        team['teammates'] = temp
        request.append(team)
    return request

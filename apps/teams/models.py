from django.db import models
#Django User
# from django.contrib.auth.models import User
from apps.users.models import Profile

# Create your models here.
#Teams
class Team(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to='static/images/', blank=True)
    name = models.CharField(max_length=50, unique=True)
    created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name='team_created_by')
    modified = models.DateField(auto_now=True)
    modified_by = models.ForeignKey(Profile,null=True, on_delete=models.SET_NULL, related_name='team_modified_by')
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

#Users in teams
class Member(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return '{}-{}'.format(self.team.name,self.user.user.name)

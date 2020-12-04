#standard libraries
import json
#django libraries
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
#Get models
from apps.users.models import User, Profile

# Create your views here.
def users(request):
    request = {'request' : 'Everything is ok in Users'}
    return JsonResponse(request)

"""
Show user with user_is
ex.
show/1
"""
def show(request, user_id):
    user_id = int(user_id)
    user = User.objects.filter(id=user_id)
    data = json.loads(serializers.serialize('json',user))
    if not data:
        data={'request':'User is Not found'}
    return JsonResponse(data, safe=False)

"""
Show all users
"""
def show_all(request):
    users = User.objects.all()
    data = json.loads(serializers.serialize('json',users))
    return JsonResponse(data, safe=False)

"""
Create new user
request -> {"email":"EMAIL",
              "name":"NAME",
              "password":"PSSWD",!!!! <-THIS IS ONLY A DEMONSTRATIVE TRIAL
              "is_admin":"True or False"}
"""
def create(request):
    if request.method == 'POST':
        # Create new user
        # Check if user email already exists in DB
        try :
            user = User.objects.create_user(email=request.POST['email'],
                                            password=request.POST['password'])
        except:
            data ={'data' : 'E-mail is alredy in user'}
            return JsonResponse(data, safe=False)
        #Set user name
        user.name = request.POST['name']
        user.save()
        # Create new teammate profile for user
        new_member = Profile.objects.create()
        new_member.user = user
        # Verify if this new user is admin
        if 'is_admin' in request.POST:
            if request.POST['is_admin'] == "False":
                new_member.is_admin = False
            if request.POST['is_admin'] == "True":
                new_member.is_admin = True
        new_member.save()
        return redirect(f'/users/show/{user.id}')

"""
Delete user
request -> {'name' : 'NAME_USER _2_DELETE'}
"""
def delete(request):
    if request.method == 'POST':
        #Disable user
        try:
            user = User.objects.get(name=request.POST['name'])
        except:
            data={'data' : 'User not found'}
            return JsonResponse(data)
        if user.is_active == False:
             data={'data' : 'User was deleted previosly'}
             return JsonResponse(data)
        user.is_active = False
        user.save()
        return redirect(f'/users/show/{user.id}')

"""
Modify user
request -> {"name" : "USER_NAME_2_MODIFY",
              "new_name":"NEW_NAME",
              "new_email":"NEW_EMAIL",
              "is_admin":"True or False"}
"""
def modify(request):
    if request.method == 'POST':
        #Disable user
        try:
            user = User.objects.get(name=request.POST['name'])
        except:
            data={'data' : 'User not found'}
            return JsonResponse(data)
        if user.is_active == False:
             data={'data' : 'User was deleted previosly'}
             return JsonResponse(data)
        #set modifications if they exist
        if 'new_name' in request.POST:
            user.name = request.POST['new_name']

        if 'new_email' in request.POST:
            user.email = request.POST['new_email']

        if 'is_admin' in request.POST:
            if request.POST['is_admin'] == "False":
                user.is_admin = False
            if request.POST['is_admin'] == "True":
                user.is_admin = True
        user.save()
        return redirect(f'/users/show/{user.id}')

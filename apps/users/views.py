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
structure -> {"email":"EMAIL",
              "name":"NAME",
              "password":"PSSWD",!!!! <-THIS IS ONLY A DEMONSTRATIVE TRIAL
              "is_admin":"True or False"}
ex.
{"email":"email@email.com","name":"SamSam","password":"trecetrecedos","is_admin":"True"}
"""
def create(request, new_user):
    #Check if dict has a correct structure
    try:
        new_user = json.loads(new_user)
    except:
        data = {'request' :'Bad Query'}
        return JsonResponse(data)
    #Check if dict has all required elements
    required_field=['email', 'name', 'password']
    for field in required_field:
        if not field in new_user:
            data ={'data' : f'{field} field must be added in request'}
            return JsonResponse(data, safe=False)
    # Create new user
    # Check if user email already exists in DB
    try :
        user = User.objects.create_user(email=new_user['email'],
                                        password=new_user['password'])
    except:
        data ={'data' : 'E-mail is alredy in user'}
        return JsonResponse(data, safe=False)
    #Set user name
    user.name = new_user['name']
    user.save()
    # Create new teammate profile for user
    new_member = Profile.objects.create()
    new_member.user = user
    # Verify if this new user is admin
    if 'is_admin' in new_user:
        if new_user['is_admin'] == "False":
            new_member.is_admin = False
        if new_user['is_admin'] == "True":
            new_member.is_admin = True
    new_member.save()
    return redirect(f'/users/show/{user.id}')

"""
Delete user
structure -> {'name' : 'NAME_USER _2_DELETE'}
ex.
delete/{"name":"SamSam"}
"""
def delete(request, user2delete):
    #Check if dict has a correct structure
    try:
        user2delete = json.loads(user2delete)
    except:
        data = {'request' :'Bad Query'}
        return JsonResponse(data)
    #Check if dict has all required elements
    required_field=['name']
    for field in required_field:
        if not field in user2delete:
            data ={'data' : f'{field} field must be added in request'}
            return JsonResponse(data, safe=False)
    #Disable user
    try:
        user = User.objects.get(name=user2delete['name'])
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
structure -> {"name" : "USER_NAME_2_MODIFY",
              "new_name":"NEW_NAME",
              "new_email":"NEW_EMAIL",
              "is_admin":"True or False"}
ex.
modify/{"name":"SamSam","new_name":"Armando"}
"""
def modify(request, user2modify):
    #Check if dict has a correct structure
    try:
        user2modify = json.loads(user2modify)
    except:
        data = {'request' :'Bad Query'}
        return JsonResponse(data)
    #Check if dict has all required elements
    required_field=['name']
    for field in required_field:
        if not field in user2modify:
            data ={'data' : f'{field} field must be added in request'}
            return JsonResponse(data, safe=False)
    #Disable user
    try:
        user = User.objects.get(name=user2modify['name'])
    except:
        data={'data' : 'User not found'}
        return JsonResponse(data)
    if user.is_active == False:
         data={'data' : 'User was deleted previosly'}
         return JsonResponse(data)
    #set modifications if they exist
    if 'new_name' in user2modify:
        user.name = user2modify['new_name']
    if 'new_email' in user2modify:
        user.email = user2modify['new_email']
    if 'is_admin' in user2modify:
        if user2modify['is_admin'] == "False":
            user.is_admin = False
        if user2modify['is_admin'] == "True":
            user.is_admin = True
    user.save()
    return redirect(f'/users/show/{user.id}')

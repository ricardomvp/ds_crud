from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def users(request):
    request = {'request' : 'Everything is ok in Users'}
    return JsonResponse(request)
    # return render(request, 'users/login.html')

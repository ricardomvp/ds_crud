from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def home(request):
    request = {'request' : 'Everything is ok'}
    return JsonResponse(request)
    # return render(request, 'users/login.html')

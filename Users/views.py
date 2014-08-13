from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse


def UserLogin(request):
    return HttpResponse('')


def UserLogout(request):
    return HttpResponse('')


#@login_required(login_url="user_login")
def index(request):
    return render(request, "Users/index.html")
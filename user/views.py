from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def user_handler(request):
    return render(request, "user.html")


def user_registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username, email, password)
        user.save()
    return render(request, "registration.html")


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, "user.html", {'log_in': 'Log in - SUCCESSFUL!'})
        else:
            return render(request, "registration.html")
    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect('/user/login/')

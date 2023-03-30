from django.shortcuts import render
from django.http import HttpResponse


def user_handler(request):
    return HttpResponse("Hello, User")

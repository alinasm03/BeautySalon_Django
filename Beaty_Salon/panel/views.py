from django.shortcuts import render
from django.http import HttpResponse


def root_handler(request):
    return HttpResponse("Hello panel")


def bookings_handler(request):
    return HttpResponse("Bookings")


def specialist_handler(request):
    return HttpResponse("Hello specialist_handler!")


def specialist_id_handler(request, specialist_id):
    return HttpResponse(f"Hello specialist_handler, {specialist_id}")

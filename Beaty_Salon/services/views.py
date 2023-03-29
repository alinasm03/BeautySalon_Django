from django.shortcuts import render
from django.http import HttpResponse


def root_handler(request):
    return render(request, "index.html")


def service_name_handler(request, service_name):
    return HttpResponse(f"Service - {service_name}")


def specialist_handler(request):
    return HttpResponse("Hello specialist!")


def specialist_id_handler(request, specialist_id):
    return HttpResponse(f"Hello specialist, {specialist_id}")


def booking_handler(request):
    return HttpResponse("Booking")

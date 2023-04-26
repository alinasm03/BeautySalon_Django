import datetime
from django.shortcuts import render
from django.http import HttpResponse
from services.models import Service, Master, Schedule, Booking
from services.free_time import calc_free_windows


def service_handler(request):
    date_start = datetime.date.today()
    date_end = datetime.date.today() + datetime.timedelta(days=7)
    # day_of_week = date_start.weekday()
    # monday = date_start - datetime.timedelta(days=day_of_week)
    # sunday = date_start + datetime.timedelta(days=6 - day_of_week)
    # week = f'{monday} -- {sunday}'
    week = f'{date_start} -- {date_end}'

    calendars = Schedule.objects.filter(date__gte=date_start,
                                        date__lte=date_end
                                        ).all()
    available_masters = Master.objects.filter(schedule__in=calendars, status=1).distinct()
    services = Service.objects.filter(master__in=available_masters).distinct()
    return render(request, 'service.html', {'services': list(services), 'week': week})


def service_name_handler(request, service_id):
    bookings = Booking.objects.all()
    if request.method == 'POST':
        bookings = Booking(
            master=Master.objects.get(name=request.POST['master_name']),
            service=Service.objects.filter(id=service_id).first(),
            client=1,
            date=request.POST['date'],
            status=True
        )
        bookings.save()
        bookings.refresh_from_db()
    bookings = Booking.objects.all()
    date_start = datetime.date.today()
    date_end = datetime.date.today() + datetime.timedelta(days=7)
    week = f'{date_start} -- {date_end}'

    service_name = Service.objects.filter(id=service_id).first()
    master_calendars = Schedule.objects.filter(date__gte=date_start,
                                               date__lte=date_end).all()
    # select masters, who do this procedure
    available_masters_service = []
    for master in master_calendars:
        master_id_services = Master.objects.get(id=master.master_id).services.filter(id=service_id)
        if master_id_services:
            available_masters_service.append(master)
    free_windows_all_masters = []
    for free_window_for_master in available_masters_service:
        time_start_date = datetime.datetime.combine(free_window_for_master.date, free_window_for_master.time_start)
        time_end_date = datetime.datetime.combine(free_window_for_master.date, free_window_for_master.time_end)
        free_windows = calc_free_windows(
            service_name,
            free_window_for_master.master_id,
            time_start_date,
            time_end_date
        )
        dict_master_date_time = {free_window_for_master.master.name: sorted(free_windows)}
        free_windows_all_masters.append(dict_master_date_time)
    merged_dict_masters = {}
    for d in free_windows_all_masters:
        for key in d:
            if key in merged_dict_masters:
                for elem in d[key]:
                    merged_dict_masters[key].append(elem)
            else:
                merged_dict_masters[key] = d[key]

    sorted_list_dict_free_windows_all_masters = []
    sorted_dict_free_windows_all_masters = {}
    for key in merged_dict_masters:
        sorted_dict_free_windows_all_masters[key] = sorted(merged_dict_masters[key])
        sorted_list_dict_free_windows_all_masters.append({key: sorted(merged_dict_masters[key])})
    return render(request, 'one_service.html', {'week': week,
                                                'service_name': service_name,
                                                'sorted_list_dict_free_windows_all_masters': sorted_list_dict_free_windows_all_masters
                                                })


def specialist_handler(request):
    date_start = datetime.date.today()
    date_end = datetime.date.today() + datetime.timedelta(days=7)
    week = f'{date_start} -- {date_end}'

    calendars = Schedule.objects.filter(date__gte=date_start,
                                        date__lte=date_end
                                        ).all()
    available_masters = Master.objects.filter(schedule__in=calendars, status=1).distinct()
    return render(request, 'specialist.html', {'specialists': list(available_masters), 'week': week})


def specialist_id_handler(request, specialist_id):
    bookings = Booking.objects.all()
    if request.method == 'POST':
        bookings = Booking(
            master=Master.objects.filter(id=specialist_id).first(),
            service=Service.objects.get(name=request.POST['service_name']),
            client=1,
            date=request.POST['date'],
            status=True
        )
        bookings.save()
        bookings.refresh_from_db()
    bookings = Booking.objects.all()
    date_start = datetime.date.today()
    date_end = datetime.date.today() + datetime.timedelta(days=7)
    week = f'{date_start} -- {date_end}'

    master_name = Master.objects.get(id=specialist_id)
    masters_all_services = Master.objects.get(id=specialist_id).services.all()
    master_calendars = Schedule.objects.filter(master_id=specialist_id,
                                               date__gte=date_start,
                                               date__lte=date_end).all()
    free_windows_all_services = []
    for service in masters_all_services:
        for day in master_calendars:
            time_start_date = datetime.datetime.combine(day.date, day.time_start)
            time_end_date = datetime.datetime.combine(day.date, day.time_end)
            free_windows_by_day = calc_free_windows(
                service,
                specialist_id,
                time_start_date,
                time_end_date
            )
            dict_service_date_time = {service: sorted(free_windows_by_day)}
            free_windows_all_services.append(dict_service_date_time)
    merged_dict_services = {}
    for d in free_windows_all_services:
        for key in d:
            if key in merged_dict_services:
                for elem in d[key]:
                    merged_dict_services[key].append(elem)
            else:
                merged_dict_services[key] = d[key]
    sorted_list_dict_free_windows_all_services = []
    sorted_dict_free_windows_all_masters = {}
    for key in merged_dict_services:
        sorted_dict_free_windows_all_masters[key] = sorted(merged_dict_services[key])
        sorted_list_dict_free_windows_all_services.append({key: sorted(merged_dict_services[key])})
    return render(request, 'one_master.html', {'week': week,
                                               'master_name': master_name,
                                               'sorted_list_dict_free_windows_all_services': sorted_list_dict_free_windows_all_services
                                               })

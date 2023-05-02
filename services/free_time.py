from datetime import timedelta
from services import models


def convert_period_to_set(time_start, time_end):
    time_set = set()
    while time_start <= time_end:
        time_set.add(time_start.replace(tzinfo=None))
        time_start += timedelta(minutes=15)
    return time_set


def calc_free_windows(service, specialist, workday_time_start, workday_time_end):
    free_time = []
    bookings = models.Booking.objects.filter(master=specialist, date__day=workday_time_start.day).all()
    busy_time = []
    for booking in bookings:
        booking_time_start = booking.date
        booking_time_end = booking.date + timedelta(minutes=booking.service.duration)
        busy_time.append(convert_period_to_set(booking_time_start, booking_time_end))
    day_times = sorted(convert_period_to_set(workday_time_start, workday_time_end - timedelta(minutes=service.duration)))

    for time_start in day_times:
        possible_time = convert_period_to_set(time_start, time_start + timedelta(minutes=service.duration))
        no_intersection = True
        for one_booking in busy_time:
            if len(possible_time.intersection(one_booking)) > 1:
                no_intersection = False
                break
        if no_intersection:
            free_time.append(time_start)
    return free_time


def test_calc_free_windows(bookings, service_duration, workday_time_start, workday_time_end):
    free_time = []
    busy_time = []
    for booking in bookings:
        booking_time_start = booking['date']
        booking_time_end = booking['date'] + timedelta(minutes=booking['service_duration'])
        busy_time.append(convert_period_to_set(booking_time_start, booking_time_end))
    day_times = sorted(convert_period_to_set(workday_time_start, workday_time_end - timedelta(minutes=service_duration)))

    for time_start in day_times:
        possible_time = convert_period_to_set(time_start, time_start + timedelta(minutes=service_duration))
        no_intersection = True
        for one_booking in busy_time:
            if len(possible_time.intersection(one_booking)) > 1:
                no_intersection = False
                break
        if no_intersection:
            free_time.append(time_start)
    return sorted(free_time)


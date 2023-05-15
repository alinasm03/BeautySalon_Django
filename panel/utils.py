from django.http import HttpResponse


def check_admin(func):
    def wrapper(*args, **kwargs):
        if not args[0].user.groups.filter(name='salon_admin_panel').exists():
            return HttpResponse('Немає доступу до перегляду сторінки')
        return func(*args, **kwargs)
    return wrapper

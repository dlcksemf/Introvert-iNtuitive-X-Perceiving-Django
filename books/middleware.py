import zoneinfo
from django.conf import settings
from django.utils import timezone
from django.shortcuts import redirect, render

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone', settings.TIME_ZONE)
        if tzname:
            timezone.activate(zoneinfo.ZoneInfo(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
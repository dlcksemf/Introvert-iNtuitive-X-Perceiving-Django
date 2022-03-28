import zoneinfo
from django.conf import settings
from django.utils import timezone
from django.shortcuts import redirect, render
import pytz

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timezone.activate(pytz.timezone("Asia/Seoul"))
        return self.get_response(request)
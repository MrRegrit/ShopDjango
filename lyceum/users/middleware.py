import zoneinfo

import django.utils.timezone

import users.models


class ChangeRequestUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user = users.models.User.objects.get(id=request.user.id)
        return self.get_response(request)


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            tzname = request.COOKIES.get("django_timezone")
            if tzname:
                django.utils.timezone.activate(zoneinfo.ZoneInfo(tzname))
            else:
                django.utils.timezone.deactivate()
        except Exception:
            django.utils.timezone.deactivate()

        return self.get_response(request)


__all__ = []

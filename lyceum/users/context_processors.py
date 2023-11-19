import django.http
import django.utils.timezone

import users.models


def birthday_users(request: django.http.HttpRequest):
    current_day = django.utils.timezone.now().date().day
    birthday_users = (
        users.models.User.objects.filter(profile__birthday__day=current_day)
        .order_by("?")
        .all()
    )
    return {"today_birthdays": birthday_users}


__all__ = []

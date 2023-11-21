import django.http
import django.utils.timezone

import users.models


def birthday_users(request):
    current_date = django.utils.timezone.now().date()
    birthday_users = (
        users.models.User.objects.select_related("profile")
        .filter(
            profile__birthday__day=current_date.day,
            profile__birthday__month=current_date.month,
        )
        .order_by("?")
        .only("username", "email")
        .all()
    )
    return {"today_birthdays": birthday_users}


__all__ = []

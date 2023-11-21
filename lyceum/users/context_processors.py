import django.http
import django.utils.timezone

import users.models


def birthday_users(request):
    current_date = django.utils.timezone.localdate()

    birthday_users = (
        users.models.Profile.objects
        .select_related("user")
        .filter(
            birthday__day=current_date.day,
            birthday__month=current_date.month,
        )
        .only("user__username", "user__email")
        .order_by("?")
    )

    return {"today_birthdays": birthday_users}


__all__ = []

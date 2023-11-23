import django.contrib.admin
import django.contrib.auth.admin
import django.contrib.auth.models

import users.models


class InlineProfile(django.contrib.admin.TabularInline):
    model = users.models.Profile
    fields = (
        users.models.Profile.birthday.field.name,
        users.models.Profile.image_tmb,
        users.models.Profile.coffee_count.field.name,
        users.models.Profile.attempts_count.field.name,
        users.models.Profile.reactivate_time.field.name,
    )
    readonly_fields = (
        users.models.Profile.birthday.field.name,
        users.models.Profile.image_tmb,
        users.models.Profile.coffee_count.field.name,
        users.models.Profile.reactivate_time.field.name,
        users.models.Profile.attempts_count.field.name,
    )
    can_delete = False


django.contrib.admin.site.unregister(django.contrib.auth.admin.User)


@django.contrib.admin.register(django.contrib.auth.admin.User)
class UserAdmin(django.contrib.auth.admin.UserAdmin):
    inlines = (InlineProfile,)


__all__ = []

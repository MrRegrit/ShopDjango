import users.models


def save_profile_with_user(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        profile = users.models.Profile.objects.create(user=instance)
        profile.save()


__all__ = []

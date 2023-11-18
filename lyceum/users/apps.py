import django.apps
import django.conf
import django.db.models.signals


class UsersConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = "Пользователи"

    def ready(self):
        import users.signals

        django.db.models.signals.post_save.connect(
            users.signals.save_profile_with_user,
            sender=django.conf.settings.AUTH_USER_MODEL,
        )


__all__ = []

import django.apps


class HomepageConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "homepage"
    verbose_name = "Главная страница"


__all__ = ["HomepageConfig"]

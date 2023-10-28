import django.apps


class HomepageConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "homepage"
    verbose_name = "главная страница"


__all__ = ["HomepageConfig"]

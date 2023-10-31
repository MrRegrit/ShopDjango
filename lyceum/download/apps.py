import django.apps


class DownloadConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "download"
    verbose_name = "Загрузка"


__all__ = []

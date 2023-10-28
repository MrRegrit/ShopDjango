from django.apps import AppConfig


class AboutConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "about"
    verbose_name = "о проекте"


__all__ = ["AboutConfig"]

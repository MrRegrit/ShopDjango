import django.apps


class FeedbackConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "feedback"
    verbose_name = "Обращения"


__all__ = []

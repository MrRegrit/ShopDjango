import django.db.models


class Feedback(django.db.models.Model):
    text = django.db.models.TextField(
        verbose_name="текст",
    )
    mail = django.db.models.EmailField(
        verbose_name="почта",
    )
    created_on = django.db.models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата и время создания",
        null=True,
    )

    class Meta:
        verbose_name = "обращение"
        verbose_name_plural = "обращения"


__all__ = []

import django.conf
import django.db.models


class StatusLog(django.db.models.Model):
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        verbose_name="пользователь",
        help_text="Пользователь изменивший статус обращения",
        related_name="users",
        related_query_name="user",
        editable=False,
    )
    timestamp = django.db.models.DateTimeField(
        auto_now_add=True, verbose_name="время изменения",
    )
    from_status = django.db.models.CharField(
        max_length=15, editable=False, verbose_name="статус до",
    )
    to_status = django.db.models.CharField(
        max_length=15, editable=False, verbose_name="статус после",
    )

    class Meta:
        verbose_name = "Логи"
        verbose_name_plural = "Лог"

    def __str__(self):
        return self.user.username


class Feedback(django.db.models.Model):
    name = django.db.models.CharField(
        max_length=254,
        verbose_name="имя",
    )
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
    status = django.db.models.CharField(
        default="получено",
        max_length=15,
        choices=(
            ("получено", "получено"),
            ("в обработке", "в обработке"),
            ("ответ дан", "ответ дан"),
        ),
        verbose_name="статус",
    )

    class Meta:
        verbose_name = "обращение"
        verbose_name_plural = "обращения"

    def __str__(self):
        return self.text[:20]


__all__ = []

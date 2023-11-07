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
        auto_now_add=True,
        verbose_name="время изменения",
    )
    from_status = django.db.models.CharField(
        max_length=15,
        editable=False,
        verbose_name="статус до",
        db_column="from",
    )
    to = django.db.models.CharField(
        max_length=15,
        editable=False,
        verbose_name="статус после",
    )

    class Meta:
        verbose_name = "Логи"
        verbose_name_plural = "Лог"

    def __str__(self):
        return self.user.username


class FeedbackExtra(django.db.models.Model):
    name = django.db.models.CharField(
        max_length=254,
        verbose_name="имя",
        blank=True,
    )
    mail = django.db.models.EmailField(
        verbose_name="почта",
    )

    class Meta:
        verbose_name = "данные к обращению"
        verbose_name_plural = "данные к обращениям"

    def __str__(self):
        return self.mail


class Feedback(django.db.models.Model):
    text = django.db.models.TextField(
        verbose_name="текст",
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
    extra = django.db.models.OneToOneField(
        FeedbackExtra,
        on_delete=django.db.models.CASCADE,
        related_name="feedbackExtra",
        related_query_name="FeedbackExtra",
        verbose_name="доп. данные",
    )

    class Meta:
        verbose_name = "обращение"
        verbose_name_plural = "обращения"

    def __str__(self):
        if len(str(self.text)) > 20:
            return self.text[:20] + "..."
        return self.text[:20]


class FeedbackFiles(django.db.models.Model):
    def feedback_directory_to(self, filename):
        return f"uploads/{self.feedback_id}/{filename}"

    feedback = django.db.models.ForeignKey(
        Feedback,
        on_delete=django.db.models.CASCADE,
        related_name="feedbacks",
        related_query_name="feedback",
        verbose_name="обращение",
    )
    file = django.db.models.FileField(
        upload_to=feedback_directory_to,
        verbose_name="файл",
    )

    class Meta:
        verbose_name = "файлы к обращению"
        verbose_name_plural = "файлы к обращениям"

    def __str__(self):
        return str(self.pk)


__all__ = []

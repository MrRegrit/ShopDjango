import django.conf
import django.db.models

import catalog.models


class Rating(django.db.models.Model):
    evaluation = django.db.models.IntegerField(
        choices=(
            (1, "Ненависть"),
            (2, "Неприязнь"),
            (3, "Нейтрально"),
            (4, "Обожание"),
            (5, "Любовь"),
        ),
        verbose_name="оценка",
    )
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        verbose_name="пользователь",
    )
    item = django.db.models.ForeignKey(
        catalog.models.Item,
        on_delete=django.db.models.CASCADE,
        verbose_name="товар",
    )

    class Meta:
        verbose_name = "рейтинг"
        verbose_name_plural = "рейтинги"
        constraints = [
            django.db.models.UniqueConstraint(
                "user",
                "item",
                name="unique_rating",
            ),
        ]


__all__ = []

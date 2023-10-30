import django.db.models


class PublishedAndNameAbstractModel(django.db.models.Model):
    is_published = django.db.models.BooleanField(
        default=True,
        verbose_name="опубликовано",
        help_text="Поставьте галочку, если хотите опубликовать товар",
    )
    name = django.db.models.CharField(
        max_length=150,
        verbose_name="название",
        help_text="Введите название товара. Максимум 150 символов",
        unique=True,
    )

    class Meta:
        abstract = True


__all__ = ["PublishedAndNameAbstractModel"]

import ckeditor.fields
import django.core.exceptions
import django.core.validators
import django.db.models
import django.utils.html
import sorl.thumbnail

import catalog.validators
import core.models


class Tag(core.models.PublishedAndNameAbstractModel):
    slug = django.db.models.SlugField(
        max_length=200,
        verbose_name="слаг",
        help_text="Введите только латинские буквы, "
        "цифры, знаки подчеркивания или дефис",
    )
    normalized_name = django.db.models.CharField(
        max_length=150,
        verbose_name="нормализованное имя",
        help_text="Это нормализованное имя, если вы это видите, "
        "значит что то не то)",
        unique=True,
        editable=False,
    )

    def save(self, *args, **kwargs) -> None:
        normalized_name = catalog.validators.normalize_text(self.name)
        self.normalized_name = normalized_name
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def clean(self) -> None:
        normalized_name = catalog.validators.normalize_text(self.name)
        if self.__class__.objects.filter(
            normalized_name=normalized_name,
        ).exclude(id=self.id):
            raise django.core.exceptions.ValidationError(
                "ОбЪект с похожем именем уже существует!",
            )
        self.normalized_name = normalized_name
        return super().clean()


class Category(core.models.PublishedAndNameAbstractModel):
    slug = django.db.models.SlugField(
        max_length=200,
        verbose_name="слаг",
        help_text="Введите только "
        "латинские буквы, цифры, знаки подчеркивания или дефис",
    )
    weight = django.db.models.PositiveSmallIntegerField(
        default=100,
        verbose_name="вес",
        help_text="Введите число от 1 до 32767",
        validators=[
            django.core.validators.MaxValueValidator(32767),
            django.core.validators.MinValueValidator(1),
        ],
    )
    normalized_name = django.db.models.CharField(
        max_length=150,
        verbose_name="нормализованное имя",
        help_text="Это нормализованное имя, "
        "если вы это видите, значит что то не то)",
        unique=True,
        editable=False,
    )

    def save(self, *args, **kwargs):
        normalized_name = catalog.validators.normalize_text(self.name)
        self.normalized_name = normalized_name
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def clean(self):
        normalized_name = catalog.validators.normalize_text(self.name)
        if self.__class__.objects.filter(
            normalized_name=normalized_name,
        ).exclude(id=self.id):
            raise django.core.exceptions.ValidationError(
                "ОбЪект с похожем именем уже существует!",
            )
        self.normalized_name = normalized_name
        return super().clean()


class MainImage(django.db.models.Model):
    image = django.db.models.ImageField(
        upload_to="catalog/main_images",
        help_text="загрузите главное изображение",
    )

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )

    def image_tmb(self):
        if self.image:
            return django.utils.html.mark_safe(
                f'<img src="{self.image.url}" width="50">',
            )
        return "Нет изображения"


class ItemManager(django.db.models.Manager):
    def published(self):
        return (
            self.get_queryset()
            .filter(is_published=True, category__is_published=True)
            .select_related("category")
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=Tag.objects.filter(is_published=True).only(
                        "name",
                    ),
                ),
            )
            .only("name", "text", "category__name")
        )


class Item(core.models.PublishedAndNameAbstractModel):
    objects = ItemManager()
    text = ckeditor.fields.RichTextField(
        verbose_name="текст",
        help_text="Описание должно содержать слова "
        "`превосходно` или `роскошно`",
        validators=[
            catalog.validators.ValidateMustContain("превосходно", "роскошно"),
        ],
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        verbose_name="категория",
        help_text="Выберете одну категорию",
        related_name="items",
        related_query_name="item",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        verbose_name="теги",
        help_text="Выберете теги.",
        related_name="items",
        related_query_name="item",
    )
    main_image = django.db.models.OneToOneField(
        MainImage,
        on_delete=django.db.models.SET_NULL,
        blank=True,
        null=True,
        related_name="items",
        related_query_name="item",
        verbose_name="главное изображение",
        help_text="Выберете главное изображение",
    )
    is_on_main = django.db.models.BooleanField(
        default=False,
        verbose_name="на главной",
        help_text="Поставьте галочку, "
        "если хотите разместить товар на главной странице",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def image_tmb(self):
        if self.main_image:
            return django.utils.html.mark_safe(
                f'<img src="{self.main_image.image.url}" width="50">',
            )
        return "Нет изображения"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True


class Images(django.db.models.Model):
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="images",
        related_query_name="image",
        help_text="Выберете товар",
    )
    image = django.db.models.ImageField(
        upload_to="catalog/images",
        help_text="Загрузите изображения",
    )

    class Meta:
        verbose_name = "дополнительное изображение"
        verbose_name_plural = "дополнительные изображения"

    def image_tmb(self):
        if self.image:
            return django.utils.html.mark_safe(
                f'<img src="{self.image.url}" width="50">',
            )
        return "Нет изображения"

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )


__all__ = ["Tag", "Category", "MainImage", "Item", "Images"]

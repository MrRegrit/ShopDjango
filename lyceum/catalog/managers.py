import django.core
import django.db.models
import django.utils


import catalog.models


class PublishedManager(django.db.models.Manager):
    def published(self):
        return (
            self.get_queryset()
            .filter(is_published=True, category__is_published=True)
            .select_related(catalog.models.Item.category.field.name)
            .prefetch_related(
                django.db.models.Prefetch(
                    catalog.models.Item.tags.field.name,
                    queryset=catalog.models.Tag.objects.filter(
                        is_published=True,
                    ).only(
                        catalog.models.Tag.name.field.name,
                    ),
                ),
            )
            .only(
                catalog.models.Item.name.field.name,
                catalog.models.Item.text.field.name,
                f"{catalog.models.Item.category.field.name}"
                f"__{catalog.models.Category.name.field.name}",
            )
            .order_by(
                catalog.models.Item.category.field.name,
                catalog.models.Item.name.field.name,
            )
        )


class ItemManager(PublishedManager):
    def on_main(self):
        return self.published().filter(is_on_main=True)

    def detail(self):
        return (
            self.published()
            .select_related(catalog.models.Item.main_image.field.name)
            .only(
                catalog.models.Item.name.field.name,
                catalog.models.Item.text.field.name,
                f"{catalog.models.Item.category.field.name}"
                f"__{catalog.models.Category.name.field.name}",
                f"{catalog.models.Item.main_image.field.name}"
                f"__{catalog.models.MainImage.image.field.name}",
            )
        )


__all__ = []

import django.contrib.admin

import catalog.models


class InlineImage(django.contrib.admin.TabularInline):
    model = catalog.models.Images
    readonly_fields = (catalog.models.Images.image_tmb,)


django.contrib.admin.site.register(
    catalog.models.MainImage,
    list_display=(catalog.models.MainImage.image_tmb,),
    readonly_fields=(catalog.models.MainImage.image_tmb,),
)
django.contrib.admin.site.register(
    catalog.models.Images,
    list_display=(catalog.models.Images.image_tmb,),
    readonly_fields=(catalog.models.Images.image_tmb,),
)


@django.contrib.admin.register(catalog.models.Tag)
class TagAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Tag.name.field.name,
        catalog.models.Tag.is_published.field.name,
    )
    list_editable = (catalog.models.Tag.is_published.field.name,)


@django.contrib.admin.register(catalog.models.Category)
class CategoryAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Category.name.field.name,
        catalog.models.Category.is_published.field.name,
        catalog.models.Category.weight.field.name,
    )
    list_editable = (catalog.models.Category.is_published.field.name,)


@django.contrib.admin.register(catalog.models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.image_tmb,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = ("tags",)
    inlines = [
        InlineImage,
    ]
    readonly_fields = (
        catalog.models.Item.image_tmb,
        catalog.models.Item.created_at.field.name,
        catalog.models.Item.updated_at.field.name,
    )

    fields = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.is_on_main.field.name,
        catalog.models.Item.text.field.name,
        catalog.models.Item.category.field.name,
        catalog.models.Item.tags.field.name,
        catalog.models.Item.main_image.field.name,
        catalog.models.Item.image_tmb,
        catalog.models.Item.created_at.field.name,
        catalog.models.Item.updated_at.field.name,
    )


__all__ = []

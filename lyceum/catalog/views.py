import django.db.models
import django.shortcuts

import catalog.models


def item_list(request):
    template = "catalog/item_list.html"
    items = catalog.models.Item.objects.published()
    context = {"items": items}
    return django.shortcuts.render(request, template, context)


def item_detail(request, pk):
    item = django.shortcuts.get_object_or_404(
        (
            catalog.models.Item.objects.filter(is_published=True)
            .select_related("category")
            .select_related("main_image")
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=catalog.models.Tag.objects.filter(
                        is_published=True,
                    ).only(
                        "name",
                    ),
                ),
            )
            .only(
                "name",
                "text",
                "category__name",
                "main_image__image",
            )
        ),
        pk=pk,
    )
    images = catalog.models.Images.objects.filter(item_id=pk).only("image")
    template = "catalog/item.html"
    context = {"item": item, "images": images}
    return django.shortcuts.render(request, template, context)


__all__ = [
    "item_list",
    "item_detail",
]

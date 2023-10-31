import django.db.models
import django.shortcuts
import django.utils.timezone

import catalog.models


def item_list(request):
    template = "catalog/item_list.html"
    items = catalog.models.Item.objects.published().order_by(
        "category",
        "name",
    )
    context = {"items": items, "title": "Список товаров"}
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


def item_new(request):
    template = "catalog/item_list.html"
    my_ids = (
        catalog.models.Item.objects.published()
        .filter(
            created_at__gte=(
                django.utils.timezone.now()
                - django.utils.timezone.timedelta(days=7)
            ),
        )
        .values_list("id", flat=True)
        .order_by("?")[:5]
    )
    if my_ids:
        items = (
            catalog.models.Item.objects.published()
            .filter(id__in=my_ids)
            .order_by(
                "category",
                "name",
            )
        )
    else:
        items = None
    context = {"items": items, "title": "Новинки"}
    return django.shortcuts.render(request, template, context)


def item_friday(request):
    template = "catalog/item_list.html"
    my_ids = (
        catalog.models.Item.objects.published()
        .filter(updated_at__week_day=6)
        .order_by("updated_at")
        .values_list("id", flat=True)[:5]
    )
    if my_ids:
        items = (
            catalog.models.Item.objects.published()
            .filter(id__in=my_ids)
            .order_by(
                "category",
                "name",
            )
        )
    else:
        items = None
    context = {"items": items, "title": "Пятница"}
    return django.shortcuts.render(request, template, context)


def item_unverified(request):
    template = "catalog/item_list.html"
    items = (
        catalog.models.Item.objects.published()
        .filter(created_at=django.db.models.F("updated_at"))
        .order_by(
            "category",
            "name",
        )
    )
    context = {"items": items, "title": "Непроверенное"}
    return django.shortcuts.render(request, template, context)


__all__ = [
    "item_list",
    "item_detail",
]

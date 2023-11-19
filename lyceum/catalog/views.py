import django.db.models
import django.shortcuts
import django.utils.timezone
import django.views.generic

import catalog.models


class ItemListView(django.views.generic.ListView):
    model = catalog.models.Item
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    extra_context = {"title": "Список товаров"}

    def get_queryset(self):
        return self.model.objects.published().order_by(
            "category",
            "name",
        )


class ItemDetailView(django.views.generic.DetailView):
    model = catalog.models.Item
    template_name = "catalog/item.html"
    context_object_name = "item"

    def get_queryset(self):
        return (
            self.model.objects.filter(is_published=True)
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
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images"] = catalog.models.Images.objects.filter(
            item_id=context["item"],
        ).only("image")
        return context


class ItemNewView(django.views.generic.ListView):
    model = catalog.models.Item
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    extra_context = {"title": "Новинки"}

    def get_queryset(self):
        my_ids = (
            self.model.objects.published()
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
            return (
                self.model.objects.published()
                .filter(id__in=my_ids)
                .order_by(
                    "category",
                    "name",
                )
            )
        return None


class ItemFridayView(django.views.generic.ListView):
    model = catalog.models.Item
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    extra_context = {"title": "Пятница"}

    def get_queryset(self):
        my_ids = (
            catalog.models.Item.objects.published()
            .filter(updated_at__week_day=6)
            .order_by("updated_at")
            .values_list("id", flat=True)[:5]
        )
        if my_ids:
            return (
                catalog.models.Item.objects.published()
                .filter(id__in=my_ids)
                .order_by(
                    "category",
                    "name",
                )
            )
        return None


class ItemUnverifiedView(django.views.generic.ListView):
    model = catalog.models.Item
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    extra_context = {"title": "Непроверенное"}

    def get_queryset(self):
        return (
            self.model.objects.published()
            .filter(created_at=django.db.models.F("updated_at"))
            .order_by(
                "category",
                "name",
            )
        )


__all__ = []

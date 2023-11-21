import django.contrib.auth.decorators
import django.db.models
import django.shortcuts

import django.urls
import django.utils.timezone
import django.views.generic

import catalog.models
import rating.forms
import rating.models


class ItemDeleteCommentView(django.views.generic.RedirectView):
    query_string = True
    pattern_name = "catalog:item_detail"

    def get_redirect_url(self, *args, **kwargs):
        rating.models.Rating.objects.filter(
            item=kwargs["pk"],
            user=self.request.user,
        ).delete()
        return super().get_redirect_url(*args, **kwargs)


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


class ItemDetailView(
    django.views.generic.DetailView,
    django.views.generic.FormView,
):
    model = catalog.models.Item
    template_name = "catalog/item.html"
    context_object_name = "item"
    form_class = rating.forms.RatingForm

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
            item=context[self.context_object_name],
        ).only("image")
        context["ratings"] = rating.models.Rating.objects.filter(
            item=context[self.context_object_name],
        ).aggregate(
            django.db.models.Avg(rating.models.Rating.evaluation.field.name),
        )[
            f"{rating.models.Rating.evaluation.field.name}__avg"
        ]
        if self.request.user.is_authenticated:
            context["user_rating"] = (
                rating.models.Rating.objects.filter(
                    item=context[self.context_object_name],
                    user=self.request.user,
                )
                .only(rating.models.Rating.evaluation.field.name)
                .first()
            )
        return context

    def form_valid(self, form):
        rating.models.Rating.objects.update_or_create(
            user=self.request.user,
            item=self.model.objects.get(pk=self.kwargs["pk"]),
            defaults={
                rating.models.Rating.evaluation.field.name: (
                    form.cleaned_data.get(
                        rating.models.Rating.evaluation.field.name,
                    )
                ),
            },
        )
        return super().form_valid(form)

    def get_success_url(self):
        return django.urls.reverse(
            "catalog:item_detail",
            args=[self.kwargs["pk"]],
        )


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

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
        return self.model.objects.published()


class ItemDetailView(
    django.views.generic.DetailView,
    django.views.generic.FormView,
):
    model = catalog.models.Item
    template_name = "catalog/item.html"
    context_object_name = "item"
    form_class = rating.forms.RatingForm

    def get_queryset(self):
        return self.model.objects.detail()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["images"] = catalog.models.Images.objects.filter(
            item=context[self.context_object_name],
        ).only("image")

        queryset = rating.models.Rating.objects.filter(
            item=context[self.context_object_name],
        ).aggregate(
            django.db.models.Avg(rating.models.Rating.evaluation.field.name),
            django.db.models.Count(rating.models.Rating.evaluation.field.name),
        )

        context["avg_ratings"] = queryset[
            f"{rating.models.Rating.evaluation.field.name}__avg"
        ]
        context["count_ratings"] = queryset[
            f"{rating.models.Rating.evaluation.field.name}__count"
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
                    catalog.models.Item.category.field.name,
                    catalog.models.Item.name.field.name,
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
            .order_by(catalog.models.Item.updated_at.field.name)
            .values_list("id", flat=True)[:5]
        )
        if my_ids:
            return (
                catalog.models.Item.objects.published()
                .filter(id__in=my_ids)
                .order_by(
                    catalog.models.Item.category.field.name,
                    catalog.models.Item.name.field.name,
                )
            )
        return None


class ItemUnverifiedView(django.views.generic.ListView):
    model = catalog.models.Item
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    extra_context = {"title": "Непроверенное"}

    def get_queryset(self):
        return self.model.objects.published().filter(
            created_at=django.db.models.F(
                catalog.models.Item.updated_at.field.name,
            ),
        )


__all__ = []

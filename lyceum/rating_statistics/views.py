import django.contrib.auth.decorators
import django.contrib.auth.models
import django.db.models
import django.shortcuts
import django.urls
import django.utils.timezone
import django.views.generic


import catalog.models
import rating.forms
import rating.models


class UserStatistic(
    django.views.generic.DetailView,
):
    model = django.contrib.auth.models.User
    template_name = "statistics/user_statistics.html"
    context_object_name = "user"

    def get_queryset(self):
        return self.model.objects.filter().only(
            "id",
            "username",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_rating = rating.models.Rating.objects.filter(
            user_id=context["user"],
        )
        context["average_rating"] = user_rating.aggregate(
            django.db.models.Avg("evaluation"),
        )["evaluation__avg"]
        context["ratings_number"] = user_rating.count()
        context["best_item"] = (
            user_rating.order_by("-evaluation", "-id").first().item_id
        )
        context["worse_item"] = (
            user_rating.order_by("evaluation", "-id").first().item_id
        )

        return context

    def get_success_url(self):
        return django.urls.reverse(
            "statistics:user_statistics",
            args=[self.kwargs["pk"]],
        )


class RatingStatistic(
    django.views.generic.DetailView,
):
    model = django.contrib.auth.models.User
    template_name = "statistics/rating_statistics.html"
    context_object_name = "user"

    def get_queryset(self):
        return self.model.objects.filter().only(
            "id",
            "username",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ratings"] = rating.models.Rating.objects.filter(
            user_id=context["user"],
        ).order_by("-evaluation")

        return context

    def get_success_url(self):
        return django.urls.reverse(
            "statistics:rating_statistics",
            args=[self.kwargs["pk"]],
        )


class ItemStatistic(
    django.views.generic.DetailView,
):
    model = catalog.models.Item
    template_name = "statistics/item_statistics.html"
    context_object_name = "item"

    def get_queryset(self):
        return self.model.objects.filter().only(
            "id",
            "name",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_rating = rating.models.Rating.objects.filter(
            item_id=context["item"],
        )
        context["average_rating"] = item_rating.aggregate(
            django.db.models.Avg("evaluation"),
        )["evaluation__avg"]
        context["ratings_number"] = item_rating.count()
        context["best_user"] = (
            item_rating.order_by("-evaluation", "-id").first().user_id
        )
        context["worse_user"] = (
            item_rating.order_by("evaluation", "-id").first().user_id
        )

        return context

    def get_success_url(self):
        return django.urls.reverse(
            "statistics:rating_statistics",
            args=[self.kwargs["pk"]],
        )


__all__ = []

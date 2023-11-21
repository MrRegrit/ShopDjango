import django.contrib.auth.decorators
import django.contrib.auth.models
import django.db.models
import django.shortcuts
import django.urls
import django.utils.decorators
import django.utils.timezone
import django.views.generic


import catalog.models
import rating.forms
import rating.models


class UserStatistics(
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

        user_rating = (
            rating.models.Rating.objects.filter(
                user=context["user"],
            )
            .select_related("item")
            .order_by("-evaluation", "-id")
            .only(
                rating.models.Rating.evaluation.field.name,
                f"{rating.models.Rating.item.field.name}"
                f"__{catalog.models.Item.name.field.name}",
            )
        )

        context["average_rating"] = user_rating.aggregate(
            django.db.models.Avg("evaluation"),
        )["evaluation__avg"]
        context["ratings_number"] = user_rating.count()
        context["best_item"] = user_rating.first()
        context["worse_item"] = user_rating.order_by(
            "evaluation",
            "-id",
        ).first()

        return context


@django.utils.decorators.method_decorator(
    django.contrib.auth.decorators.login_required,
    name="dispatch",
)
class ProfileStatistics(
    django.views.generic.TemplateView,
):
    model = django.contrib.auth.models.User
    template_name = "statistics/profile_statistics.html"
    context_object_name = "user"

    def get_queryset(self):
        return self.model.objects.filter().only(
            "id",
            "username",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["ratings"] = (
            rating.models.Rating.objects.filter(
                user=self.request.user,
            )
            .select_related("item")
            .order_by("-evaluation")
            .only(
                rating.models.Rating.evaluation.field.name,
                f"{rating.models.Rating.item.field.name}"
                f"__{catalog.models.Item.name.field.name}",
            )
        )

        return context


class ItemStatistics(
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
        item_rating = (
            rating.models.Rating.objects.filter(
                item=context["item"],
            )
            .select_related("user")
            .only(
                rating.models.Rating.evaluation.field.name,
                f"{rating.models.Rating.user.field.name}"
                f"__{django.contrib.auth.models.User.username.field.name}",
            )
        )

        context["average_rating"] = item_rating.aggregate(
            django.db.models.Avg("evaluation"),
        )["evaluation__avg"]
        context["ratings_number"] = item_rating.count()
        context["best_user"] = item_rating.order_by(
            "-evaluation",
            "-id",
        ).first()
        context["worse_user"] = item_rating.order_by(
            "evaluation",
            "-id",
        ).first()

        return context


__all__ = []

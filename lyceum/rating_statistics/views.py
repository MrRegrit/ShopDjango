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
            django.contrib.auth.models.User.username.field.name,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_rating = rating.models.Rating.objects.user_rating(
            context["user"],
        )
        queryset = user_rating.aggregate(
            django.db.models.Avg(rating.models.Rating.evaluation.field.name),
            django.db.models.Count(rating.models.Rating.evaluation.field.name),
        )
        context["average_rating"] = queryset[
            f"{rating.models.Rating.evaluation.field.name}__avg"
        ]
        context["ratings_number"] = queryset[
            f"{rating.models.Rating.evaluation.field.name}__count"
        ]
        context["best_item"] = user_rating.order_by(
            f"-{rating.models.Rating.evaluation.field.name}",
            f"-{rating.models.Rating.id.field.name}",
        ).first()
        context["worse_item"] = user_rating.order_by(
            rating.models.Rating.evaluation.field.name,
            f"-{rating.models.Rating.id.field.name}",
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
            django.contrib.auth.models.User.username.field.name,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["ratings"] = rating.models.Rating.objects.user_rating(
            user=self.request.user,
        ).order_by(f"-{rating.models.Rating.evaluation.field.name}")

        return context


class ItemStatistics(
    django.views.generic.DetailView,
):
    model = catalog.models.Item
    template_name = "statistics/item_statistics.html"
    context_object_name = "item"

    def get_queryset(self):
        return self.model.objects.filter().only(
            catalog.models.Item.name.field.name,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_rating = rating.models.Rating.objects.item_rating(
            item=context["item"],
        )

        queryset = item_rating.aggregate(
            django.db.models.Avg(rating.models.Rating.evaluation.field.name),
            django.db.models.Count(rating.models.Rating.evaluation.field.name),
        )
        context["average_rating"] = queryset[
            f"{rating.models.Rating.evaluation.field.name}__avg"
        ]
        context["ratings_number"] = queryset[
            f"{rating.models.Rating.evaluation.field.name}__count"
        ]
        context["best_user"] = item_rating.order_by(
            f"-{rating.models.Rating.evaluation.field.name}",
            f"-{rating.models.Rating.id.field.name}",
        ).first()
        context["worse_user"] = item_rating.order_by(
            rating.models.Rating.evaluation.field.name,
            f"-{rating.models.Rating.id.field.name}",
        ).first()

        return context


__all__ = []

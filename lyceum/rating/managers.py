import django.core
import django.db.models
import django.utils

import catalog.models
import rating.models


class RatingManager(django.db.models.Manager):
    def user_rating(self, user):
        return (
            self.get_queryset()
            .filter(
                user=user,
            )
            .select_related(rating.models.Rating.item.field.name)
            .only(
                rating.models.Rating.evaluation.field.name,
                f"{rating.models.Rating.item.field.name}"
                f"__{catalog.models.Item.name.field.name}",
            )
        )

    def item_rating(self, item):
        return (
            rating.models.Rating.objects.filter(
                item=item,
            )
            .select_related(rating.models.Rating.user.field.name)
            .only(
                rating.models.Rating.evaluation.field.name,
                f"{rating.models.Rating.user.field.name}"
                f"__{django.contrib.auth.models.User.username.field.name}",
            )
        )


__all__ = []

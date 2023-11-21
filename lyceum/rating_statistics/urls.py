import django.urls

import rating_statistics.views

app_name = "rating_statistics"

urlpatterns = [
    django.urls.path(
        "user_statistics/<int:pk>/",
        rating_statistics.views.UserStatistic.as_view(),
        name="user_statistics",
    ),
    django.urls.path(
        "profile_statistics/",
        rating_statistics.views.ProfileStatistic.as_view(),
        name="profile_statistics",
    ),
    django.urls.path(
        "item_statistics/<int:pk>/",
        rating_statistics.views.ItemStatistic.as_view(),
        name="item_statistics",
    ),
]

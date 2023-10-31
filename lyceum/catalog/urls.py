import django.urls

import catalog.views

app_name = "catalog"

urlpatterns = [
    django.urls.path("", catalog.views.item_list, name="item_list"),
    django.urls.path(
        "<int:pk>/",
        catalog.views.item_detail,
        name="item_detail",
    ),
    django.urls.path("new/", catalog.views.item_new, name="item_new"),
    django.urls.path("friday/", catalog.views.item_friday, name="item_friday"),
    django.urls.path(
        "unverified/",
        catalog.views.item_unverified,
        name="item_unverified",
    ),
]

import django.urls

import catalog.views

app_name = "catalog"

urlpatterns = [
    django.urls.path("", catalog.views.item_list, name="item_list"),
    django.urls.path(
        "<int:num>/",
        catalog.views.item_detail,
        name="item_detail",
    ),
]

import django.urls

import catalog.views

app_name = "catalog"

urlpatterns = [
    django.urls.path(
        "",
        catalog.views.ItemListView.as_view(),
        name="item_list",
    ),
    django.urls.path(
        "<int:pk>/",
        catalog.views.ItemDetailView.as_view(),
        name="item_detail",
    ),
    django.urls.path(
        "new/",
        catalog.views.ItemNewView.as_view(),
        name="item_new",
    ),
    django.urls.path(
        "friday/",
        catalog.views.ItemFridayView.as_view(),
        name="item_friday",
    ),
    django.urls.path(
        "unverified/",
        catalog.views.ItemUnverifiedView.as_view(),
        name="item_unverified",
    ),
    django.urls.path(
        "<int:pk>/delete_comment/",
        catalog.views.ItemDeleteCommentView.as_view(),
        name="item_delete_comment",
    ),
]

import django.urls

import homepage.views

app_name = "homepage"

urlpatterns = [
    django.urls.path("", homepage.views.HomeView.as_view(), name="home"),
    django.urls.path("echo/", homepage.views.EchoView.as_view(), name="echo"),
    django.urls.path(
        "echo/submit/",
        homepage.views.SubmitView.as_view(),
        name="submit",
    ),
    django.urls.path(
        "coffee/",
        homepage.views.CoffeeView.as_view(),
        name="coffee",
    ),
]

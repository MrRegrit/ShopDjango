import django.urls

import homepage.views

app_name = "homepage"

urlpatterns = [
    django.urls.path("", homepage.views.home, name="home"),
    django.urls.path("echo/", homepage.views.echo, name="echo"),
    django.urls.path("echo/submuit/", homepage.views.submit, name="submit"),
    django.urls.path("coffee/", homepage.views.coffee, name="coffee"),
]

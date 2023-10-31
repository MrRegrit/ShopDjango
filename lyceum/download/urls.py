import django.urls

import download.views

app_name = "download"

urlpatterns = [
    django.urls.path(
        "<path:filepath>/",
        download.views.download_file,
        name="download_file",
    ),
]

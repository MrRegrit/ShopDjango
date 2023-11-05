import django.conf.urls.static
import django.contrib
import django.urls

import lyceum.settings

urlpatterns = [
    django.urls.path("", django.urls.include("homepage.urls")),
    django.urls.path("catalog/", django.urls.include("catalog.urls")),
    django.urls.path("about/", django.urls.include("about.urls")),
    django.urls.path("download/", django.urls.include("download.urls")),
    django.urls.path("feedback/", django.urls.include("feedback.urls")),
    django.urls.path("admin/", django.contrib.admin.site.urls),
]

if lyceum.settings.DEBUG:
    import debug_toolbar

    urlpatterns += (
        django.urls.path(
            "__debug__/",
            django.urls.include(debug_toolbar.urls),
        ),
    )
    urlpatterns += django.conf.urls.static.static(
        lyceum.settings.MEDIA_URL,
        document_root=lyceum.settings.MEDIA_ROOT,
    )

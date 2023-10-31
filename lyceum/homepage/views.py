import http

import django.http
import django.shortcuts

import catalog.models


def home(request):
    template = "homepage/main.html"
    items = catalog.models.Item.objects.on_main()
    context = {"items": items}
    return django.shortcuts.render(request, template, context)


def coffee(request):
    return django.http.HttpResponse(
        "Я чайник",
        status=http.HTTPStatus.IM_A_TEAPOT,
    )


__all__ = []

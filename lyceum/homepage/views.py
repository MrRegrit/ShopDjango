import http

import django.http
import django.shortcuts

import catalog.views


def home(request):
    template = "homepage/main.html"
    context = {"items": catalog.views.items}
    return django.shortcuts.render(request, template, context)


def coffee(request):
    return django.http.HttpResponse(
        "Я чайник",
        status=http.HTTPStatus.IM_A_TEAPOT,
    )


__all__ = ["home", "coffee"]

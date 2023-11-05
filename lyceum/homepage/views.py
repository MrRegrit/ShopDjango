import http

import django.http
import django.shortcuts

import catalog.models
import homepage.forms


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


def echo(request):
    template = "homepage/echo.html"
    form = homepage.forms.EchoForm(request.POST or None)

    context = {
        "form": form,
    }
    return django.shortcuts.render(request, template, context)


def submit(request):
    if request.method == "POST":
        return django.http.HttpResponse(request._post.get("text"))
    return django.http.HttpResponseNotFound()


__all__ = []

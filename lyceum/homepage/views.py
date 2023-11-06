import http

import django.http
import django.shortcuts
import django.views.decorators.http

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


@django.views.decorators.http.require_GET
def echo(request):
    template = "homepage/echo.html"
    form = homepage.forms.EchoForm(request.POST or None)
    context = {
        "form": form,
    }
    return django.shortcuts.render(request, template, context)


@django.views.decorators.http.require_POST
def submit(request):
    form = homepage.forms.EchoForm(request.POST or None)

    if form.is_valid():
        text = form.cleaned_data.get("text")

        return django.http.HttpResponse(text)

    return django.http.HttpResponseNotAllowed(["POST"])


__all__ = []

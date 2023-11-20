import http

import django.http
import django.utils.decorators
import django.views.decorators.http
import django.views.generic

import catalog.models
import homepage.forms


class HomeView(django.views.generic.ListView):
    model = catalog.models.Item
    template_name = "homepage/main.html"
    context_object_name = "items"

    def get_queryset(self):
        return self.model.objects.on_main()


def coffee(request):
    if request.user.is_authenticated:
        request.user.profile.coffee_count += 1
        request.user.profile.save()
    return django.http.HttpResponse(
        "Я чайник",
        status=http.HTTPStatus.IM_A_TEAPOT,
    )


@django.utils.decorators.method_decorator(
    django.views.decorators.http.require_GET,
    name="dispatch",
)
class EchoView(django.views.generic.FormView):
    template_name = "homepage/echo.html"
    form_class = homepage.forms.EchoForm


@django.views.decorators.http.require_POST
def submit(request):
    form = homepage.forms.EchoForm(request.POST or None)

    if form.is_valid():
        text = form.cleaned_data.get("text")

        return django.http.HttpResponse(text)

    return django.http.HttpResponseBadRequest("Invalid form")


__all__ = []

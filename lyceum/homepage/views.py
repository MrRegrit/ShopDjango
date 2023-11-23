import http

import django.http
import django.template.response
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


class TemplateResponse(django.template.response.TemplateResponse):
    status_code = http.HTTPStatus.IM_A_TEAPOT


class CoffeeView(django.views.generic.TemplateView):
    response_class = TemplateResponse
    template_name = "homepage/coffee.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.profile.coffee_count += 1
            request.user.profile.save()
        return super().dispatch(request, *args, **kwargs)


@django.utils.decorators.method_decorator(
    django.views.decorators.http.require_GET,
    name="dispatch",
)
class EchoView(django.views.generic.FormView):
    template_name = "homepage/echo.html"
    form_class = homepage.forms.EchoForm


@django.utils.decorators.method_decorator(
    django.views.decorators.http.require_POST,
    name="dispatch",
)
class SubmitView(django.views.generic.FormView):
    form_class = homepage.forms.EchoForm

    def form_valid(self, form):
        text = form.cleaned_data.get("text")

        return django.http.HttpResponse(text)

    def form_invalid(self, form):
        return django.http.HttpResponseBadRequest("Invalid form")


__all__ = []

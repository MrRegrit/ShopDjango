import django.conf
import django.contrib.auth.decorators
import django.contrib.auth.models
import django.contrib.messages
import django.contrib.sites.shortcuts
import django.core.mail
import django.shortcuts
import django.utils.decorators
import django.utils.timezone
import django.views.generic

import users.forms
import users.models


class SignUpView(
    django.views.generic.FormView,
):
    template_name = "users/signup.html"
    form_class = users.forms.UserCreationForm

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")

        form_save = form.save(commit=False)
        form_save.is_active = django.conf.settings.DEFAULT_USER_IS_ACTIVE
        form_save.save()

        users.models.Profile.objects.create(user=form.instance)

        current_site = django.contrib.sites.shortcuts.get_current_site(
            self.request,
        )
        reverse_activate = django.shortcuts.reverse(
            "users:activate",
            args=[username],
        )
        url_to_confirm_register = f"https://{current_site}{reverse_activate}"
        django.core.mail.send_mail(
            "Активация аккаунта",
            f"Для активации вашего аккаунта перейдите по ссылке:"
            f"\n{url_to_confirm_register}",
            django.conf.settings.MAIL,
            [
                email,
            ],
            fail_silently=False,
        )
        django.contrib.messages.success(
            self.request,
            "Активируйте аккаунт перейдя по ссылке в почте!",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return django.urls.reverse("users:signup")


class ActivateView(django.views.generic.RedirectView):
    pattern_name = "users:login"

    def get_redirect_url(self, *args, **kwargs):
        user = django.shortcuts.get_object_or_404(
            django.contrib.auth.models.User,
            username=self.kwargs["username"],
        )
        if user.date_joined >= (
            django.utils.timezone.now()
            - django.utils.timezone.timedelta(hours=12)
        ):
            user.is_active = True
            user.save()
            django.contrib.messages.success(
                self.request,
                "Вы успешно активировали аккаунт",
            )
            return super().get_redirect_url()
        raise django.shortcuts.Http404


class ReactivateView(django.views.generic.RedirectView):
    pattern_name = "users:login"

    def get_redirect_url(self, *args, **kwargs):
        user = django.shortcuts.get_object_or_404(
            django.contrib.auth.models.User,
            username=self.kwargs["username"],
        )
        if user.profile.reactivate_time is not None:
            if user.profile.reactivate_time >= (
                django.utils.timezone.now()
                - django.utils.timezone.timedelta(weeks=1)
            ):
                user.is_active = True
                user.save()
                django.contrib.messages.success(
                    self.request,
                    "Вы успешно вернули статус активности вашему аккаунту",
                )
                user.profile.reactivate_time = None
                user.profile.save()
                return super().get_redirect_url()
        raise django.shortcuts.Http404


class UserDetailView(django.views.generic.DetailView):
    model = django.contrib.auth.models.User
    template_name = "users/user_detail.html"
    context_object_name = "user"

    def get_queryset(self):
        related_name = users.models.Profile.user.field.related_query_name()

        return users.models.User.objects.select_related("profile").only(
            f"{related_name}__{users.models.Profile.birthday.field.name}",
            f"{related_name}__{users.models.Profile.image.field.name}",
            f"{related_name}__{users.models.Profile.coffee_count.field.name}",
            self.model.email.field.name,
            self.model.last_name.field.name,
            self.model.first_name.field.name,
        )


class UserListView(django.views.generic.ListView):
    model = users.models.Profile
    template_name = "users/user_list.html"
    context_object_name = "profiles"

    def get_queryset(self):
        return (
            self.model.objects.filter(user__is_active=True)
            .select_related("user")
            .only(
                self.model.birthday.field.name,
                self.model.image.field.name,
                self.model.coffee_count.field.name,
                f"{self.model.user.field.name}__"
                f"{django.contrib.auth.models.User.email.field.name}",
                f"{self.model.user.field.name}__"
                f"{django.contrib.auth.models.User.last_name.field.name}",
                f"{self.model.user.field.name}__"
                f"{django.contrib.auth.models.User.first_name.field.name}",
            )
        )


@django.utils.decorators.method_decorator(
    django.contrib.auth.decorators.login_required,
    name="dispatch",
)
class ProfileView(django.views.generic.TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "forms" not in context:
            initial = {}
            user_profile = self.request.user.profile
            if not (user_profile.birthday is None):
                initial["birthday"] = user_profile.birthday.strftime(
                    "%Y-%m-%d",
                )
            forms = (
                users.forms.UserChangeForm(
                    self.request.POST or None,
                    instance=self.request.user,
                ),
                users.forms.ProfileChangeForm(
                    self.request.POST or None,
                    self.request.FILES or None,
                    initial=initial,
                    instance=user_profile,
                ),
            )
            context["forms"] = forms
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if all(form.is_valid() for form in context["forms"]):
            [form.save() for form in context["forms"]]
            return django.shortcuts.redirect(
                django.shortcuts.reverse("users:profile"),
            )
        return django.shortcuts.render(request, self.template_name, context)


__all__ = []

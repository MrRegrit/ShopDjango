import django.conf
import django.contrib.auth.decorators
import django.contrib.auth.models
import django.contrib.messages
import django.contrib.sites.shortcuts
import django.core.mail
import django.shortcuts
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
        url_to_confirm_register = f"{current_site}{reverse_activate}"
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


def activate(request, username):
    user = django.shortcuts.get_object_or_404(
        django.contrib.auth.models.User,
        username=username,
    )
    if user.date_joined >= (
        django.utils.timezone.now() - django.utils.timezone.timedelta(hours=12)
    ):
        user.is_active = True
        user.save()
        django.contrib.messages.success(
            request,
            "Вы успешно активировали аккаунт",
        )
        return django.shortcuts.redirect("users:login")
    raise django.shortcuts.Http404


def reactivate(request, username):
    user = django.shortcuts.get_object_or_404(
        django.contrib.auth.models.User,
        username=username,
    )
    if user.profile.reactivate_time is not None:
        if user.profile.reactivate_time >= (
            django.utils.timezone.now()
            - django.utils.timezone.timedelta(weeks=1)
        ):
            user.is_active = True
            user.save()
            django.contrib.messages.success(
                request,
                "Вы успешно вернули статус активности вашему аккаунту",
            )
            user.profile.reactivate_time = None
            user.profile.save()
            return django.shortcuts.redirect("users:login")
    raise django.shortcuts.Http404


def user_detail(request, pk):
    template = "users/user_detail.html"
    profile = django.shortcuts.get_object_or_404(
        users.models.Profile.objects.select_related("user").only(
            "birthday",
            "image",
            "coffee_count",
            "user__email",
            "user__last_name",
            "user__first_name",
        ),
        user__pk=pk,
    )
    context = {"profile": profile}
    return django.shortcuts.render(request, template, context)


class UserListView(django.views.generic.ListView):
    model = users.models.Profile
    template_name = "users/user_list.html"
    context_object_name = "profiles"

    def get_queryset(self):
        return (
            self.model.objects.filter(user__is_active=True)
            .select_related("user")
            .only(
                "birthday",
                "image",
                "coffee_count",
                "user__email",
                "user__last_name",
                "user__first_name",
            )
        )


@django.contrib.auth.decorators.login_required
def profile(request):
    template = "users/profile.html"
    initial = {}
    user_profile = request.user.profile
    if not (user_profile.birthday is None):
        initial["birthday"] = user_profile.birthday.strftime("%Y-%m-%d")
    forms = (
        users.forms.UserChangeForm(
            request.POST or None,
            instance=request.user,
        ),
        users.forms.ProfileChangeForm(
            request.POST or None,
            request.FILES or None,
            initial=initial,
            instance=user_profile,
        ),
    )
    if request.method == "POST" and all(form.is_valid() for form in forms):
        [form.save() for form in forms]
        return django.shortcuts.redirect(
            django.shortcuts.reverse("users:profile"),
        )

    context = {"forms": forms}
    return django.shortcuts.render(request, template, context)


__all__ = []

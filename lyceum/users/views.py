import django.conf
import django.contrib.auth.decorators
import django.contrib.auth.models
import django.contrib.messages
import django.contrib.sites.shortcuts
import django.core.mail
import django.shortcuts
import django.utils.timezone


import users.forms
import users.models


def signup(request):
    template = "users/signup.html"
    form = users.forms.UserCreationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")

            form_save = form.save(commit=False)
            form_save.is_active = django.conf.settings.DEFAULT_USER_IS_ACTIVE
            form_save.save()

            users.models.Profile.objects.create(user=form.instance)

            current_site = django.contrib.sites.shortcuts.get_current_site(
                request,
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
                request,
                "Активируйте аккаунт перейдя по ссылке в почте!",
            )
            return django.shortcuts.redirect("users:signup")

    context = {
        "form": form,
    }
    return django.shortcuts.render(request, template, context)


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


def user_list(request):
    template = "users/user_list.html"
    profiles = (
        users.models.Profile.objects.filter(user__is_active=True)
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
    context = {"profiles": profiles}
    return django.shortcuts.render(request, template, context)


@django.contrib.auth.decorators.login_required
def profile(request):
    template = "users/profile.html"
    forms = (
        users.forms.UserChangeForm(
            request.POST or None,
            instance=request.user,
        ),
        users.forms.ProfileChangeForm(
            request.POST or None,
            request.FILES or None,
            instance=users.models.Profile.objects.get(
                user=request.user.id,
            ),
        ),
    )
    if request.method == "POST" and all([form.is_valid() for form in forms]):
        [form.save() for form in forms]
        return django.shortcuts.redirect(
            django.shortcuts.reverse("users:profile"),
        )

    context = {"forms": forms}
    return django.shortcuts.render(request, template, context)


__all__ = []

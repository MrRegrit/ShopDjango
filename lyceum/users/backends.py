import django.conf
import django.contrib.auth
import django.contrib.auth.backends
import django.contrib.sites.shortcuts
import django.core.mail
import django.db.models
import django.shortcuts
import django.utils.timezone


def normalize_email(email):
    email = email.replace("@ya.ru", "@yandex.ru")
    if "+" in email:
        email = email[: email.index("+")] + email[email.index("@") :]
    if "@gmail.com" in email:
        email = email.replace("@gmail.com", "").replace(".", "") + "@gmail.com"
    elif "@yandex.ru" in email:
        email = (
            email.replace("@yandex.ru", "").replace(".", "-") + "@yandex.ru"
        )
    return email.lower()


class EmailOrUsernameModelBackend(django.contrib.auth.backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = django.contrib.auth.get_user_model()
        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        users = user_model._default_manager.filter(
            django.db.models.Q(**{user_model.USERNAME_FIELD: username})
            | django.db.models.Q(email__iexact=normalize_email(username)),
        )
        for user in set(users):
            if user.check_password(password):
                user.profile.attempts_count = 0
                user.profile.save()
                return user

            user.profile.attempts_count += 1

            if (
                user.profile.attempts_count
                >= django.conf.settings.MAX_AUTH_ATTEMPTS
            ):
                if user.is_active:
                    user.is_active = False
                    user.save()

                    user.profile.reactivate_time = django.utils.timezone.now()

                    current_site = (
                        django.contrib.sites.shortcuts.get_current_site(
                            request,
                        )
                    )
                    reverse_reactivate = django.shortcuts.reverse(
                        "users:reactivate",
                        args=[user.username],
                    )
                    url_to_confirm_register = (
                        f"{current_site}{reverse_reactivate}"
                    )
                    django.core.mail.send_mail(
                        "Попытка взлома",
                        f"На ваш аккаунт пытались войти слишком много раз. "
                        f"Для восстановления активности вашего "
                        f"аккаунта перейдите по ссылке"
                        f"\n{url_to_confirm_register}",
                        django.conf.settings.MAIL,
                        [
                            user.email,
                        ],
                        fail_silently=False,
                    )
            user.profile.save()
        if not users:
            user_model().set_password(password)
        return None


__all__ = []

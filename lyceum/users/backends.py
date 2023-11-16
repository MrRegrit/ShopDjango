import django.conf
import django.contrib.auth
import django.contrib.auth.backends
import django.contrib.sites.shortcuts
import django.core.mail
import django.db.models
import django.shortcuts
import django.utils.timezone

import users.models as users_models


class EmailOrUsernameModelBackend(django.contrib.auth.backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = users_models.User
        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        if username is None or password is None:
            return None
        try:
            if "@" in username:
                user = user_model.objects.by_mail(username)
            else:
                user = user_model.objects.get(username=username)
        except user_model.DoesNotExist:
            user_model().set_password(password)
        else:
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


__all__ = []

import django.contrib.auth
import django.contrib.auth.backends
import django.db.models


class EmailOrUsernameModelBackend(django.contrib.auth.backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = django.contrib.auth.get_user_model()
        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        users = user_model._default_manager.filter(
            django.db.models.Q(**{user_model.USERNAME_FIELD: username})
            | django.db.models.Q(email__iexact=username),
        )
        for user in users:
            if user.check_password(password):
                return user
        if not users:
            user_model().set_password(password)
        return None


__all__ = []

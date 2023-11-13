import unittest.mock

import django.conf
import django.contrib.auth.models
import django.forms.models
import django.test
import django.urls
import django.utils.timezone

import users.forms
import users.models


class FormTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = users.forms.UserCreationForm()

    def test_create_signup_with_empty_fields(self):
        form_data = {
            "email": "",
            "username": "",
            "password1": "",
            "password2": "",
        }

        response = django.test.Client().post(
            django.urls.reverse("users:signup"),
            data=form_data,
        )
        self.assertFormError(
            response,
            "form",
            "password1",
            "Обязательное поле.",
        )
        self.assertFormError(
            response,
            "form",
            "username",
            "Обязательное поле.",
        )

    @django.test.override_settings(
        DEFAULT_USER_IS_ACTIVE=False,
    )
    def test_create_user_with_valid_fields(self):
        users_count = django.contrib.auth.models.User.objects.count()

        new_user = {
            "email": "test@test.com",
            "username": "test",
            "password1": "sdvfga2#QAZ",
            "password2": "sdvfga2#QAZ",
        }

        django.test.Client().post(
            django.urls.reverse("users:signup"),
            data=new_user,
        )

        self.assertEqual(
            users_count + 1,
            django.contrib.auth.models.User.objects.count(),
        )

        self.assertEqual(
            new_user["username"],
            django.contrib.auth.models.User.objects.last().username,
        )

        self.assertEqual(
            new_user["email"],
            django.contrib.auth.models.User.objects.last().email,
        )

    def test_create_signup_without_email_fields(self):
        users_count = django.contrib.auth.models.User.objects.count()

        new_user = {
            "email": "",
            "username": "test",
            "password1": "sdvfga2#QAZ",
            "password2": "sdvfga2#QAZ",
        }

        django.test.Client().post(
            django.urls.reverse("users:signup"),
            data=new_user,
        )

        self.assertEqual(
            users_count,
            django.contrib.auth.models.User.objects.count(),
        )

    @django.test.override_settings(
        DEFAULT_USER_IS_ACTIVE=False,
    )
    def test_activate_new_user(self):
        new_user = {
            "email": "test@test.com",
            "username": "test",
            "password1": "sdvfga2#QAZ",
            "password2": "sdvfga2#QAZ",
        }

        django.test.Client().post(
            django.urls.reverse("users:signup"),
            data=new_user,
        )

        self.assertEqual(
            False,
            django.contrib.auth.models.User.objects.last().is_active,
        )

        django.test.Client().get(
            django.urls.reverse(
                "users:activate",
                args=[django.contrib.auth.models.User.objects.last().username],
            ),
        )
        self.assertEqual(
            True,
            django.contrib.auth.models.User.objects.last().is_active,
        )

    @django.test.override_settings(
        DEFAULT_USER_IS_ACTIVE=True,
    )
    def test_default_activate_new_user(self):
        new_user = {
            "email": "test@test.com",
            "username": "test",
            "password1": "sdvfga2#QAZ",
            "password2": "sdvfga2#QAZ",
        }

        django.test.Client().post(
            django.urls.reverse("users:signup"),
            data=new_user,
        )

        self.assertEqual(
            True,
            django.contrib.auth.models.User.objects.last().is_active,
        )

        django.test.Client().get(
            django.urls.reverse(
                "users:activate",
                args=[django.contrib.auth.models.User.objects.last().username],
            ),
        )
        self.assertEqual(
            True,
            django.contrib.auth.models.User.objects.last().is_active,
        )

    def test_timeout_activate_new_user(self):
        new_user = {
            "email": "test@test.com",
            "username": "test",
            "password": "sdvfga2#QAZ",
        }

        mocked = django.utils.timezone.datetime(
            2023,
            1,
            1,
            10,
            tzinfo=django.utils.timezone.utc,
        )
        with unittest.mock.patch(
            "django.utils.timezone.now",
            unittest.mock.Mock(return_value=mocked),
        ):
            django.contrib.auth.models.User.objects.create(
                **new_user,
                date_joined=django.utils.timezone.now(),
                is_active=False,
            )

        mocked = django.utils.timezone.datetime(
            2023,
            2,
            2,
            23,
            tzinfo=django.utils.timezone.utc,
        )
        with unittest.mock.patch(
            "django.utils.timezone.now",
            unittest.mock.Mock(return_value=mocked),
        ):
            django.test.Client().get(
                django.urls.reverse(
                    "users:activate",
                    args=[
                        (django.contrib.auth.models.User)
                        .objects.last()
                        .username,
                    ],
                ),
            )

        self.assertEqual(
            False,
            django.contrib.auth.models.User.objects.last().is_active,
        )


__all__ = []

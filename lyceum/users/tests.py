import unittest.mock

import django.conf
import django.contrib.auth.models
import django.contrib.auth.views
import django.forms.models
import django.test
import django.urls
import django.utils.timezone
import parameterized

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

    @django.test.override_settings(
        DEFAULT_USER_IS_ACTIVE=True,
    )
    def test_login_with_mail_or_username(self):
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
        user_with_mail = {
            "username": "test@test.com",
            "password": "sdvfga2#QAZ",
        }
        user_with_username = {
            "username": "test",
            "password": "sdvfga2#QAZ",
        }
        self.client.login(**user_with_mail)
        response = self.client.get(
            django.urls.reverse("homepage:home"),
        )
        self.assertEqual(new_user["email"], response.context["user"].email)
        self.client.logout()

        self.client.login(**user_with_username)
        response = self.client.get(
            django.urls.reverse("homepage:home"),
        )
        self.assertEqual(new_user["email"], response.context["user"].email)

    @parameterized.parameterized.expand(
        [
            ("t.e.s.t+test@gmail.com", "test@gmail.com"),
            ("t.e.s.t+test+test@ya.ru", "t-e-s-t@yandex.ru"),
        ],
    )
    def test_normalize_email(self, email, norm_email):
        new_user = {
            "email": email,
            "username": "test",
            "password1": "sdvfga2#QAZ",
            "password2": "sdvfga2#QAZ",
        }
        django.test.Client().post(
            django.urls.reverse("users:signup"),
            data=new_user,
        )
        self.assertEqual(
            django.contrib.auth.models.User.objects.last().email,
            norm_email,
        )
        self.client.login(username=email, password=new_user["password1"])
        response = self.client.get(
            django.urls.reverse("homepage:home"),
        )
        self.assertEqual(response.context["user"].email, norm_email)

    @django.test.override_settings(
        MAX_AUTH_ATTEMPTS=3,
    )
    def test_deactivate_user_attempts(self):
        new_user = {
            "email": "test@test.com",
            "username": "test",
            "password1": "sdvfga2#QAZ",
            "password2": "sdvfga2#QAZ",
        }
        login_user = {
            "username": "test",
            "password": "123432",
        }

        django.test.Client().post(
            django.urls.reverse("users:signup"),
            data=new_user,
        )
        for i in range(3):
            django.test.Client().post(
                django.urls.reverse("users:login"),
                data=login_user,
            )

        self.assertEqual(
            django.contrib.auth.models.User.objects.last().is_active,
            False,
        )

        django.test.Client().get(
            django.urls.reverse(
                "users:reactivate",
                args=[django.contrib.auth.models.User.objects.last().username],
            ),
        )

        self.assertEqual(
            django.contrib.auth.models.User.objects.last().is_active,
            True,
        )


__all__ = []

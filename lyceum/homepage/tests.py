import http

import django.test
import django.urls


class StaticURLTests(django.test.TestCase):
    def test_homepage_endpoint(self):
        response = django.test.Client().get(
            django.urls.reverse("homepage:home"),
        )
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_coffee_endpoint(self):
        response = django.test.Client().get(
            django.urls.reverse("homepage:coffee"),
        )
        self.assertContains(
            response,
            "Я чайник",
            status_code=http.HTTPStatus.IM_A_TEAPOT,
        )


__all__ = []

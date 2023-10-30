import http
import random

import django.test
import django.urls
import parameterized


class StaticURLTests(django.test.TestCase):
    def test_catalog_list_endpoint(self):
        response = django.test.Client().get(
            django.urls.reverse("catalog:item_list"),
        )
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    @parameterized.parameterized.expand(
        [
            ("0", http.HTTPStatus.NOT_FOUND),
            ("01", http.HTTPStatus.NOT_FOUND),
            ("010", http.HTTPStatus.NOT_FOUND),
            (10, http.HTTPStatus.NOT_FOUND),
            (100, http.HTTPStatus.NOT_FOUND),
            (random.randint(1, 100000), http.HTTPStatus.NOT_FOUND),
        ],
    )
    def test_catalog_deatail_positive_endpoint(self, value, status_code):
        response = django.test.Client().get(
            django.urls.reverse("catalog:item_detail", args=[value]),
        )
        self.assertEqual(response.status_code, status_code)

    @parameterized.parameterized.expand(
        [
            ("str",),
            ("1.1",),
            ("-0",),
            ("-987",),
            ("012qwerty",),
            ("qwer123qwer",),
            ("qwert5",),
            ("123qwe123",),
            ("123%",),
            ("0$",),
        ],
    )
    def test_catalog_deatail_negative_endpoint(self, value):
        with self.assertRaises(django.urls.exceptions.NoReverseMatch):
            django.test.Client().get(
                django.urls.reverse("catalog:item_detail", args=[value]),
            )


__all__ = []

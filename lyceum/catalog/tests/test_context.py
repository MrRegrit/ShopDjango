import django.db.models.query
import django.test
import django.urls
import parameterized

import catalog.models


class ContextTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.published_category = catalog.models.Category.objects.create(
            is_published=True,
            name="Тестовая опубликованная категория",
            slug="published_category",
            weight=100,
        )
        cls.unpublished_category = catalog.models.Category.objects.create(
            is_published=False,
            name="Тестовая неопубликованная категория",
            slug="unpublished_category",
            weight=100,
        )
        cls.published_tag = catalog.models.Tag.objects.create(
            is_published=True,
            name="Тестовый опубликованный тег",
            slug="published_tag",
        )
        cls.unpublished_tag = catalog.models.Tag.objects.create(
            is_published=False,
            name="Тестовый неопубликованный тег",
            slug="published_tag",
        )
        cls.published_item_with_publ_category_on_main = (
            catalog.models.Item.objects.create(
                is_on_main=True,
                is_published=True,
                name="Тестовый опубликованный товар с опубликованной "
                "категорией на главной",
                text="превосходно",
                category=cls.published_category,
            )
        )
        cls.published_item_with_publ_category_not_on_main = (
            catalog.models.Item.objects.create(
                is_published=True,
                name="Тестовый опубликованный товар с опубликованной "
                "категорией на неглавной",
                text="превосходно",
                category=cls.published_category,
            )
        )
        cls.unpublished_item_with_publ_category = (
            catalog.models.Item.objects.create(
                is_published=False,
                name="Тестовый неопубликованный товар"
                " с опубликованной категорией",
                text="превосходно",
                category=cls.published_category,
            )
        )
        cls.published_item_with_unpubl_category = (
            catalog.models.Item.objects.create(
                is_published=True,
                name="Тестовый опубликованный товар"
                " с неопубликованной категорией",
                text="превосходно",
                category=cls.unpublished_category,
            )
        )
        cls.unpublished_item_with_unpubl_category = (
            catalog.models.Item.objects.create(
                is_published=False,
                name="Тестовый неопубликованный"
                " товар неопубликованной категорией",
                text="превосходно",
                category=cls.unpublished_category,
            )
        )

        cls.published_category.save()
        cls.unpublished_category.save()

        cls.published_tag.save()
        cls.unpublished_tag.save()

        cls.published_item_with_publ_category_on_main.clean()
        cls.published_item_with_publ_category_on_main.save()

        cls.published_item_with_publ_category_not_on_main.clean()
        cls.published_item_with_publ_category_not_on_main.save()

        cls.published_item_with_unpubl_category.clean()
        cls.published_item_with_unpubl_category.save()

        cls.unpublished_item_with_publ_category.clean()
        cls.unpublished_item_with_publ_category.save()

        cls.unpublished_item_with_unpubl_category.clean()
        cls.unpublished_item_with_unpubl_category.save()

        cls.published_item_with_publ_category_on_main.tags.add(
            cls.published_tag.pk,
        )
        cls.published_item_with_publ_category_on_main.tags.add(
            cls.unpublished_tag.pk,
        )

        cls.published_item_with_publ_category_not_on_main.tags.add(
            cls.published_tag.pk,
        )
        cls.published_item_with_publ_category_not_on_main.tags.add(
            cls.unpublished_tag.pk,
        )

    def test_show_correct_context(self):
        response = django.test.Client().get(
            django.urls.reverse("catalog:item_list"),
        )
        self.assertIsInstance(
            response.context["items"],
            django.db.models.query.QuerySet,
        )

    def test_count_item(self):
        response = django.test.Client().get(
            django.urls.reverse("catalog:item_list"),
        )
        items = response.context["items"]
        self.assertEqual(len(items), 2)

    @parameterized.parameterized.expand(
        [
            ("is_published",),
            ("is_on_main",),
            ("images",),
            ("main_image",),
            ("weight",),
            ("slug",),
            ("normalized_name",),
        ],
    )
    def test_fields_not_in_item(self, field):
        response = django.test.Client().get(
            django.urls.reverse("catalog:item_list"),
        )
        items = response.context["items"]
        for item in items:
            self.assertNotIn(field, item.__dict__)
            self.assertNotIn(field, item.category.__dict__)

    @parameterized.parameterized.expand(
        [
            ("id",),
            ("text",),
            ("category_id",),
            ("_prefetched_objects_cache",),
        ],
    )
    def test_fields_in_item(self, field):
        response = django.test.Client().get(
            django.urls.reverse("catalog:item_list"),
        )
        items = response.context["items"]
        for item in items:
            self.assertIn(field, item.__dict__)


__all__ = []

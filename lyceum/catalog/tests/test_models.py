import django.core
import django.test
import parameterized

import catalog.models


class ModelsTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.category = catalog.models.Category.objects.create(
            is_published=True,
            name="Тестовая категория",
            slug="test-category-slug",
            weight=100,
        )
        cls.tag = catalog.models.Tag.objects.create(
            is_published=True,
            name="Тестовый тег",
            slug="test-tag-slug",
        )

    def test_unable_create_without_special_words(self):
        item_count = catalog.models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                name="Тестовый товар",
                category=self.category,
                text="хихихихихи, я ошибка, как и ты)",
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(ModelsTests.tag)

        self.assertEqual(catalog.models.Item.objects.count(), item_count)

    @parameterized.parameterized.expand(
        [
            ("Превосходно"),
            ("Роскошно"),
            ("Превсоходно и очень роскошно"),
        ],
    )
    def test_create(self, text):
        item_count = catalog.models.Item.objects.count()

        self.item = catalog.models.Item(
            name="Тестовый товар",
            category=self.category,
            text=text,
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(ModelsTests.tag)
        self.assertEqual(catalog.models.Item.objects.count(), item_count + 1)

    @parameterized.parameterized.expand(
        [
            ("Тестовый тег!"),
            ("тестовыйтег"),
            ("тесто вый .---тег!%:"),
        ],
    )
    def test_create_tag_with_invalid_name(self, tag_name):
        tag_count = catalog.models.Tag.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.tag = catalog.models.Tag(
                name=tag_name,
                slug="sluuuug",
            )
            self.tag.full_clean()
            self.tag.save()
        self.assertEqual(catalog.models.Tag.objects.count(), tag_count)

    @parameterized.parameterized.expand(
        [
            ("Тестовый тег1!"),
            ("тестовыйтег2"),
            ("тесто вый .---тег3!%:"),
        ],
    )
    def test_create_tag_with_valid_name(self, tag_name):
        tag_count = catalog.models.Tag.objects.count()
        self.tag = catalog.models.Tag(
            name=tag_name,
            slug="sluuuug",
        )
        self.tag.full_clean()
        self.tag.save()
        self.assertEqual(catalog.models.Tag.objects.count(), tag_count + 1)

    @parameterized.parameterized.expand(
        [
            ("Тестовая категория!"),
            ("тестоваякатегория"),
            ("Т.ест ов !ая кат.егор _-ия"),
        ],
    )
    def test_create_category_with_invalid_name(self, category_name):
        category_count = catalog.models.Category.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.category = catalog.models.Category(
                name=category_name,
                slug="sluuuug",
                weight=50,
            )
            self.category.full_clean()
            self.category.save()
        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count,
        )

    @parameterized.parameterized.expand(
        [
            ("Тестовая категория1!"),
            ("тестоваякатегория2"),
            ("Т.ест ов !ая кат.егор _-ия3"),
        ],
    )
    def test_create_category_with_valid_name(self, category_name):
        category_count = catalog.models.Category.objects.count()
        self.category = catalog.models.Category(
            name=category_name,
            slug="sluuuug",
            weight=50,
        )
        self.category.full_clean()
        self.category.save()
        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count + 1,
        )


__all__ = []

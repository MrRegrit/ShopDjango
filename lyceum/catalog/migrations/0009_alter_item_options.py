# Generated by Django 4.2 on 2023-10-30 05:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0008_item_is_on_main_alter_category_is_published_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="item",
            options={
                "ordering": ("name",),
                "verbose_name": "товар",
                "verbose_name_plural": "товары",
            },
        ),
    ]

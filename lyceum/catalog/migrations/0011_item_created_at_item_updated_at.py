# Generated by Django 4.2 on 2023-10-31 07:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0010_alter_category_normalized_name_alter_images_item_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="item",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]

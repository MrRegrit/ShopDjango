# Generated by Django 4.2 on 2023-10-24 17:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0002_alter_mainimage_options_alter_images_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="normalized_name",
            field=models.CharField(
                max_length=150, unique=True, verbose_name="Нормализованное имя"
            ),
        ),
    ]

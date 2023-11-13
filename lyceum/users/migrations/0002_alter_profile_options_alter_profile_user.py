# Generated by Django 4.2 on 2023-11-12 11:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="profile",
            options={
                "verbose_name": "Дополнительное поле",
                "verbose_name_plural": "Дополнительные поля",
            },
        ),
        migrations.AlterField(
            model_name="profile",
            name="user",
            field=models.OneToOneField(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="profiles",
                related_query_name="profile",
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
    ]
# Generated by Django 4.2 on 2023-11-06 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("feedback", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="feedback",
            name="status",
            field=models.CharField(
                choices=[
                    ("получено", "получено"),
                    ("в обработке", "в обработке"),
                    ("ответ дан", "ответ дан"),
                ],
                default="получено",
                max_length=15,
            ),
        ),
        migrations.CreateModel(
            name="StatusLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("from_status", models.CharField(max_length=15)),
                ("to_status", models.CharField(max_length=15)),
                (
                    "user",
                    models.ForeignKey(
                        help_text="Пользователь изменивший статус обращения",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="users",
                        related_query_name="user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="пользователь",
                    ),
                ),
            ],
        ),
    ]
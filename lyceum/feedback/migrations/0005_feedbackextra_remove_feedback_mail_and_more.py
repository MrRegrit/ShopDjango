# Generated by Django 4.2 on 2023-11-07 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("feedback", "0004_rename_to_status_statuslog_to_alter_feedback_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="FeedbackExtra",
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
                (
                    "name",
                    models.CharField(blank=True, max_length=254, verbose_name="имя"),
                ),
                ("mail", models.EmailField(max_length=254, verbose_name="почта")),
            ],
        ),
        migrations.RemoveField(
            model_name="feedback",
            name="mail",
        ),
        migrations.RemoveField(
            model_name="feedback",
            name="name",
        ),
        migrations.CreateModel(
            name="FeedbackFiles",
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
                (
                    "file",
                    models.FileField(
                        upload_to="uploads/<django.db.models.fields.related.ForeignKey>/"
                    ),
                ),
                (
                    "feedback",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="feedback.feedback",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="feedback",
            name="extra",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="feedback.feedbackextra",
            ),
        ),
    ]
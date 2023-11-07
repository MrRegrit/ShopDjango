# Generated by Django 4.2 on 2023-11-07 15:52

from django.db import migrations, models
import django.db.models.deletion
import feedback.models


class Migration(migrations.Migration):
    dependencies = [
        ("feedback", "0007_alter_feedbackextra_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="extra",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="feedbackExtra",
                related_query_name="FeedbackExtra",
                to="feedback.feedbackextra",
                verbose_name="доп. данные",
            ),
        ),
        migrations.AlterField(
            model_name="feedbackfiles",
            name="feedback",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="feedbacks",
                related_query_name="feedback",
                to="feedback.feedback",
                verbose_name="обращение",
            ),
        ),
        migrations.AlterField(
            model_name="feedbackfiles",
            name="file",
            field=models.FileField(
                upload_to=feedback.models.feedback_directory_path, verbose_name="файл"
            ),
        ),
    ]

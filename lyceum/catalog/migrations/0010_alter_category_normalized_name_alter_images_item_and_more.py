# Generated by Django 4.2 on 2023-10-30 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0009_alter_item_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="normalized_name",
            field=models.CharField(
                editable=False,
                help_text="Это нормализованное имя, если вы это видите, значит что то не то)",
                max_length=150,
                verbose_name="нормализованное имя",
            ),
        ),
        migrations.AlterField(
            model_name="images",
            name="item",
            field=models.ForeignKey(
                help_text="Выберете товар",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                related_query_name="image",
                to="catalog.item",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="category",
            field=models.ForeignKey(
                help_text="Выберете одну категорию",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                related_query_name="item",
                to="catalog.category",
                verbose_name="категория",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="main_image",
            field=models.OneToOneField(
                blank=True,
                help_text="Выберете главное изображение",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="items",
                related_query_name="item",
                to="catalog.mainimage",
                verbose_name="главное изображение",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="tags",
            field=models.ManyToManyField(
                help_text="Выберете теги.",
                related_name="items",
                related_query_name="item",
                to="catalog.tag",
                verbose_name="теги",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="normalized_name",
            field=models.CharField(
                editable=False,
                help_text="Это нормализованное имя, если вы это видите, значит что то не то)",
                max_length=150,
                verbose_name="нормализованное имя",
            ),
        ),
    ]

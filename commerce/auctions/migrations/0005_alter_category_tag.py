# Generated by Django 4.2.13 on 2024-09-12 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0004_alter_category_tag"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="tag",
            field=models.CharField(max_length=32),
        ),
    ]

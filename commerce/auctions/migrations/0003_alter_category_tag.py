# Generated by Django 4.2.13 on 2024-09-12 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_category_listing_usercomment_bid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="tag",
            field=models.CharField(max_length=32),
        ),
    ]

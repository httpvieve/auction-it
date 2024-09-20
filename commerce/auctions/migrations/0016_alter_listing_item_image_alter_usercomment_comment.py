# Generated by Django 4.2.13 on 2024-09-20 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0015_alter_usercomment_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="item_image",
            field=models.URLField(
                blank=True,
                default="https://curie.pnnl.gov/sites/default/files/default_images/default-image_0.jpeg",
            ),
        ),
        migrations.AlterField(
            model_name="usercomment",
            name="comment",
            field=models.TextField(null=True),
        ),
    ]

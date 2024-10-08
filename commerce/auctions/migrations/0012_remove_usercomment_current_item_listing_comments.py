# Generated by Django 4.2.13 on 2024-09-15 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0011_alter_listing_auction_winner_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="usercomment",
            name="current_item",
        ),
        migrations.AddField(
            model_name="listing",
            name="comments",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="comments",
                to="auctions.usercomment",
            ),
        ),
    ]

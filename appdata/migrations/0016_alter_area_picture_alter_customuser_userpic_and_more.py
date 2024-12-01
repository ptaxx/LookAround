# Generated by Django 5.1.3 on 2024-12-01 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appdata", "0015_remove_game_finishing_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="area",
            name="picture",
            field=models.ImageField(blank=True, null=True, upload_to="area_pictures"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="userpic",
            field=models.ImageField(
                blank=True,
                default="static/images/default_userpic.png",
                null=True,
                upload_to="profile_pictures",
            ),
        ),
        migrations.AlterField(
            model_name="venue",
            name="picture",
            field=models.ImageField(blank=True, null=True, upload_to="venue_pictures"),
        ),
    ]

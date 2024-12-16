# Generated by Django 5.1.3 on 2024-12-15 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appdata", "0016_alter_area_picture_alter_customuser_userpic_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="activity",
            name="is_location",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="activity",
            name="latitude",
            field=models.FloatField(default=0, max_length=50),
        ),
        migrations.AddField(
            model_name="activity",
            name="longitude",
            field=models.FloatField(default=0, max_length=50),
        ),
    ]
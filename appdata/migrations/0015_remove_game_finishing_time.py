# Generated by Django 5.1.3 on 2024-11-30 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appdata', '0014_alter_area_picture_alter_customuser_userpic_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='finishing_time',
        ),
    ]

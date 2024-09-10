# Generated by Django 5.0.6 on 2024-09-09 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_appconfig'),
    ]

    operations = [
        migrations.AddField(
            model_name='appconfig',
            name='order_app_enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='appconfig',
            name='trip_app_enabled',
            field=models.BooleanField(default=True),
        ),
    ]

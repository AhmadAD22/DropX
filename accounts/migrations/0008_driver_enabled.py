# Generated by Django 5.0.6 on 2024-06-13 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_car_carmodel_driver_carmodel_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='enabled',
            field=models.BooleanField(default=False),
        ),
    ]

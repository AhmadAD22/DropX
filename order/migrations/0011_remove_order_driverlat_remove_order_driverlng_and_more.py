# Generated by Django 5.0.6 on 2024-07-21 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_alter_trip_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='driverLat',
        ),
        migrations.RemoveField(
            model_name='order',
            name='driverLng',
        ),
        migrations.AddField(
            model_name='order',
            name='destinationName',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='destinationPhone',
            field=models.CharField(max_length=15, null=True),
        ),
    ]

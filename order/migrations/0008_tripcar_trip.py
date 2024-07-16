# Generated by Django 5.0.6 on 2024-07-13 10:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0032_restaurantsubscription'),
        ('order', '0007_alter_cartaccessory_quantity_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='TripCar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='Car Trip')),
                ('price_per_km', models.FloatField()),
                ('name', models.CharField(max_length=50)),
                ('average_speed', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField()),
                ('tripDate', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled'), ('REJECTED', 'Rejected')], max_length=20)),
                ('sourceLat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('sourceLng', models.DecimalField(decimal_places=6, max_digits=9)),
                ('sourceAddress', models.CharField(max_length=100)),
                ('destinationLat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('destinationLng', models.DecimalField(decimal_places=6, max_digits=9)),
                ('destinationAddress', models.CharField(max_length=100)),
                ('distance', models.FloatField()),
                ('price', models.FloatField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.client')),
                ('coupon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.coupon')),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.driver')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tripcar', to='order.tripcar')),
            ],
            options={
                'ordering': ['-createdAt'],
            },
        ),
    ]

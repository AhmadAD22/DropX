# Generated by Django 5.0.6 on 2024-08-24 02:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0039_alter_pendingdriver_carcategory'),
        ('order', '0017_order_checkoutat'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='trip',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.trip'),
        ),
    ]

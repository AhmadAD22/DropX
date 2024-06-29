# Generated by Django 5.0.6 on 2024-06-29 10:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_restaurant_restaurantstatus'),
        ('order', '0004_cartitem_note_orderitem_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.order'),
        ),
    ]

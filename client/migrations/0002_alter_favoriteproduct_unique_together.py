# Generated by Django 5.0.6 on 2024-07-06 00:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_notification_order'),
        ('client', '0001_initial'),
        ('restaurant', '0019_alter_commonquestion_restaurant'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favoriteproduct',
            unique_together={('client', 'product')},
        ),
    ]

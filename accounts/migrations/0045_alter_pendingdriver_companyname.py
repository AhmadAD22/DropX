# Generated by Django 5.0.6 on 2024-09-04 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0044_user_notificationenabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendingdriver',
            name='companyName',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

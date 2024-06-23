# Generated by Django 5.0.6 on 2024-06-12 09:13

import accounts.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_membersservicesubscription_orderservicesubscription_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carType', models.CharField(max_length=50)),
                ('carModel', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='OTPRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('code', models.CharField(default=accounts.models.otpCodeDefault, max_length=4)),
                ('expireAt', models.DateTimeField(default=accounts.models.expireDefault)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('REGISTER', 'Register'), ('RESET_PHONE', 'Reset Phone'), ('FORGET_PASSWORD', 'Forget Password')], max_length=18)),
                ('isUsed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PendingClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(max_length=60)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('otp', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pendingClient', to='accounts.otprequest')),
            ],
        ),
        migrations.DeleteModel(
            name='ServiceSubscription',
        ),
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Client', 'verbose_name_plural': 'Client'},
        ),
        migrations.AlterModelOptions(
            name='driver',
            options={'verbose_name': 'Driver', 'verbose_name_plural': 'Driver'},
        ),
        migrations.AlterModelOptions(
            name='restaurant',
            options={'verbose_name': 'Restaurant', 'verbose_name_plural': 'Restaurant'},
        ),
        migrations.RenameField(
            model_name='driver',
            old_name='carType',
            new_name='carColor',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='manufactureYear',
        ),
        migrations.AddField(
            model_name='driver',
            name='carCategory',
            field=models.CharField(choices=[('إقتصادي', 'Economical'), ('سيدان\\كروس', 'Sedan'), ('كبيرة 6 ركاب', 'Big'), ('أعمال', 'Business')], default=1, max_length=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='driver',
            name='carName',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='driver',
            name='car',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.car'),
            preserve_default=False,
        ),
    ]

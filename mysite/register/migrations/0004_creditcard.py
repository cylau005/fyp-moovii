# Generated by Django 4.0.2 on 2022-03-07 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('register', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cc_number', models.CharField(max_length=16, unique=True, verbose_name='cc_number')),
                ('cc_name', models.CharField(max_length=40, unique=True, verbose_name='cc_name')),
                ('cc_expirydate', models.CharField(max_length=10, unique=True, verbose_name='cc_expirydate')),
                ('cc_cvv', models.CharField(max_length=3, unique=True, verbose_name='cc_expirydate')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
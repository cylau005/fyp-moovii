# Generated by Django 4.0.2 on 2022-05-21 04:56

import creditcards.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cc_number', creditcards.models.CardNumberField(max_length=25, verbose_name='card number')),
                ('cc_name', models.CharField(max_length=40, verbose_name='cc_name')),
                ('cc_expirydate', creditcards.models.CardExpiryField(verbose_name='expiration date')),
                ('cc_cvv', creditcards.models.SecurityCodeField(max_length=4, verbose_name='security code')),
                ('subscription_enddate', models.DateTimeField(default=datetime.datetime(2022, 6, 20, 4, 56, 33, 282201, tzinfo=utc))),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BankIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_enddate', models.DateTimeField(default=datetime.datetime(2022, 6, 20, 4, 56, 33, 282201, tzinfo=utc))),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField(blank=True, default=None, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=6)),
                ('genres', models.CharField(choices=[('Adventure', 'Adventure'), ('Comedy', 'Comedy'), ('Action', 'Action'), ('Drama', 'Drama'), ('Crime', 'Crime'), ('Children', 'Children'), ('Mystery', 'Mystery'), ('Documentary', 'Documentary'), ('Animation', 'Animation'), ('Thriller', 'Thriller'), ('Horror', 'Horror'), ('Fantasy', 'Fantasy'), ('Western', 'Western'), ('Film-Noir', 'Film-Noir'), ('Romance', 'Romance'), ('War', 'War'), ('Sci-Fi', 'Sci-Fi'), ('Musical', 'Musical')], max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

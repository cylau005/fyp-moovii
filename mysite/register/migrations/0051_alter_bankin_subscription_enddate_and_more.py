# Generated by Django 4.0.2 on 2022-05-07 08:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0050_alter_account_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankin',
            name='subscription_enddate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 6, 8, 13, 46, 644053, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='subscription_enddate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 6, 8, 13, 46, 644053, tzinfo=utc)),
        ),
    ]

# Generated by Django 4.0.2 on 2022-04-23 00:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0040_alter_bankin_subscription_enddate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankin',
            name='subscription_enddate',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 23, 0, 58, 10, 907566, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='subscription_enddate',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 23, 0, 58, 10, 906556, tzinfo=utc)),
        ),
    ]

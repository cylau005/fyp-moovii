# Generated by Django 4.0.2 on 2022-05-07 08:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0051_alter_bankin_subscription_enddate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankin',
            name='subscription_enddate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 6, 8, 51, 17, 654614, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='subscription_enddate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 6, 8, 51, 17, 654614, tzinfo=utc)),
        ),
    ]

# Generated by Django 4.0.2 on 2022-03-31 12:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0030_alter_creditcard_cc_cvv_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcard',
            name='subscription_enddate',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 30, 12, 46, 21, 930497, tzinfo=utc)),
        ),
    ]
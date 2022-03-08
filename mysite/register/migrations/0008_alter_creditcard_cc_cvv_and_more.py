# Generated by Django 4.0.2 on 2022-03-08 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0007_alter_creditcard_cc_expirydate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcard',
            name='cc_cvv',
            field=models.CharField(max_length=3, unique=True, verbose_name='cc_cvv'),
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='cc_expirydate',
            field=models.CharField(max_length=4, unique=True, verbose_name='cc_expirydate'),
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='cc_number',
            field=models.CharField(max_length=16, unique=True, verbose_name='cc_number'),
        ),
    ]

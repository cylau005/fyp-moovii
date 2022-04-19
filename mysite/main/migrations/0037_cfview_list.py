# Generated by Django 4.0.2 on 2022-04-19 13:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0036_alter_reward_point_redeem_item_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CFView_List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField(blank=True, default=None, null=True)),
                ('movie_name', models.CharField(blank=True, max_length=100)),
                ('movie_image_url', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
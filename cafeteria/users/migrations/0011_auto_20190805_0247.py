# Generated by Django 2.2.1 on 2019-08-04 17:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20190609_1721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followers',
        ),
        migrations.AddField(
            model_name='user',
            name='follower',
            field=models.ManyToManyField(blank=True, related_name='_user_follower_+', to=settings.AUTH_USER_MODEL),
        ),
    ]

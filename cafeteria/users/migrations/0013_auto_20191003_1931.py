# Generated by Django 2.2.1 on 2019-10-03 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20190805_0248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='stdntnum',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]

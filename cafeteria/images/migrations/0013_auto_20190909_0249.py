# Generated by Django 2.2.1 on 2019-09-08 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0012_comment_refer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
# Generated by Django 2.2.1 on 2019-09-08 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0014_auto_20190909_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='images', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(max_length=30),
        ),
    ]
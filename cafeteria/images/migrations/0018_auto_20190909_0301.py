# Generated by Django 2.2.1 on 2019-09-08 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0017_auto_20190909_0300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='referComment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='commentOnComment', to='images.Comment'),
        ),
    ]

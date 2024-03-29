# Generated by Django 2.2.1 on 2019-10-09 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ddoock', models.CharField(max_length=1024)),
                ('il', models.CharField(max_length=1024)),
                ('rice', models.CharField(max_length=1024)),
                ('noodle', models.CharField(max_length=1024)),
                ('yang', models.CharField(max_length=1024)),
                ('faculty_menu', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='TuData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tu_id', models.CharField(max_length=50)),
                ('tu_password', models.CharField(max_length=50)),
                ('first_day', models.CharField(max_length=10)),
                ('second_day', models.CharField(max_length=10)),
                ('apply_text', models.TextField()),
                ('message', models.TextField(blank=True)),
            ],
        ),
    ]

from django.db import models

# Create your models here.


class TuData(models.Model):
    tu_id = models.CharField(max_length=50)
    tu_password = models.CharField(max_length=50)
    first_day = models.CharField(max_length=10)
    second_day = models.CharField(max_length=10)
    apply_text = models.TextField()
    message = models.TextField(blank=True)


class RestaurantData(models.Model):
    ddoock = models.CharField(max_length=1024)
    il = models.CharField(max_length=1024)
    rice = models.CharField(max_length=1024)
    noodle = models.CharField(max_length=1024)
    yang = models.CharField(max_length=1024)
    faculty_menu = models.CharField(max_length=1024)

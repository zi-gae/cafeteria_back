from django.db import models

# Create your models here.


class TimeStampeModel(models.Model):
    create_at: models.DateTimeField(auto_now_add=True)
    update_at: models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        # abstract meta class 는 데이터베이스를 생성하지 않음
        # 다른 데이터베이스를 위한 base 로 사용


class Image(TimeStampeModel):
    file = models.ImageField()
    content = models.TextField(max_length=700)


class Comment(TimeStampeModel):
    message = models.TextField(max_length=150)

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from instar.users import models as user_models
# Create your models here.


@python_2_unicode_compatible
class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        # abstract meta class 는 데이터베이스를 생성하지 않음
        # 다른 데이터베이스를 위한 base 로 사용


@python_2_unicode_compatible
class Image(TimeStampedModel):

    """ Image  conctent Model """
    # json 으로 변경
    file = models.ImageField()
    title = models.CharField(max_length=30)
    content = models.TextField(max_length=700)
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True, related_name="images")

    @property
    def like_count(self):
        return self.likes.all().count()

    def __str__(self):
        return '{} - {}'.format(self.content, self.creator.username)


@python_2_unicode_compatible
class Comment(TimeStampedModel):

    """ Comment  Model """
    message = models.TextField(max_length=150)
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True)
    image = models.ForeignKey(Image, on_delete=models.PROTECT, null=True, related_name='comments')

    def __str__(self):
        return 'msg: {}'.format(self.message)


@python_2_unicode_compatible
class Like(TimeStampedModel):

    """ Like Model """
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True)
    image = models.ForeignKey(Image, on_delete=models.PROTECT, null=True, related_name='likes')

    def __str__(self):
        return 'user:{} - image:{}'.format(self.creator.username, self.image.content)

    class Meta:
        ordering = ['-created_at']

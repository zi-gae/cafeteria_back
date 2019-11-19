from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from cafeteria.users import models as user_models
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


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

    TYPE_CHOICES = (
        ("free", "자유게시판"),
        ("review", "강의 후기 & 팁"),
        ("sale", "중고 장터")
        # 실제 값  ,  보여지는 값
    )
    kinds = models.CharField(max_length=120, choices=TYPE_CHOICES, default="free")
    file = ProcessedImageField(
        format='JPEG',
        options={'quality': 30}, null=True, blank=True)
    title = models.CharField(max_length=1000)
    content = models.TextField(max_length=1000)
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, related_name="images")
    anonymous = models.BooleanField(blank=True, default=True)

    @property
    def like_count(self):
        return self.likes.all().count()

    @property
    def comment_count(self):
        return self.comments.all().count()

    @property
    def natural_time(self):
        return naturaltime(self.created_at)

    def __str__(self):
        return '{} - {}'.format(self.content, self.creator.username)


@python_2_unicode_compatible
class Comment(TimeStampedModel):

    """ Comment  Model """
    message = models.TextField(max_length=1000)
    anonymous = models.BooleanField(blank=True, default=True)
    commentShow = models.BooleanField(blank=True, default=True)
    creator = models.ForeignKey(user_models.User, on_delete=models.CASCADE, null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, related_name='comments')
    referComment = models.ForeignKey("self", on_delete=models.CASCADE,
                                     null=True, blank=True, related_name='commentOnComment')

    def natural_time(self):
        return naturaltime(self.created_at)

    def __str__(self):
        return 'msg: {}'.format(self.message)


@python_2_unicode_compatible
class Like(TimeStampedModel):

    """ Like Model """
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, related_name='likes')

    def __str__(self):
        return 'user:{} - image:{}'.format(self.creator.username, self.image.content)

    class Meta:
        ordering = ['-created_at']

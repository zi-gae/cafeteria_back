from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


class User(AbstractUser):
    """ Users Models """
    profile_image = ProcessedImageField(
        processors=[Thumbnail(100, 100)],
        format='JPEG',
        options={'quality': 60}, null=True, blank=True)
    name = CharField(_("Name of User"), null=True, max_length=255, blank=True, unique=True)
    stdntnum = models.IntegerField(null=True, blank=True, unique=True)
    bio = models.TextField(null=True)
    push_token = models.TextField(null=True, blank=True, unique=False)
    student_card = models.ImageField(blank=True, null=True)
    univ_authentication = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    @property
    def postCount(self):
        return self.images.all().count()

    @property
    def followersCount(self):
        return self.followers.all().count()

    @property
    def followingCount(self):
        return self.following.all().count()

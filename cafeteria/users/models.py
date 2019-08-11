from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    """ Users Models """
    profile_image = models.ImageField(null=True, blank=True)
    name = CharField(_("Name of User"), null=True, max_length=255, blank=True)
    stdntnum = models.IntegerField(null=True)
    bio = models.TextField(null=True)
    followers = models.ManyToManyField("self", blank=True)
    following = models.ManyToManyField("self", blank=True)

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

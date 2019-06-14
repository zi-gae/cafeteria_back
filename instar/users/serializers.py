from rest_framework import serializers
from . import models
from instar.images import serializers as image_serialiazers


class UserProfileSerializer(serializers.ModelSerializer):

    images = image_serialiazers.UserProfileImageSerializer(many=True)

    class Meta:
        model = models.User

        fields = (
            "username",
            "name",
            "bio",
            "stdntnum",
            "post_count",
            "followers_count",
            "following_count",
            "images"
        )


class ExploreUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            "id",
            "profile_image",
            "username",
            "name"
        )

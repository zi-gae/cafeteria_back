from rest_framework import serializers
from . import models
from cafeteria.images import serializers as image_serialiazers


class UserProfileSerializer(serializers.ModelSerializer):

    images = image_serialiazers.UserProfileImageSerializer(many=True)

    class Meta:
        # postCount = serializers.ReadOnlyField()
        # followersCount = serializers.ReadOnlyField()
        # followingCount = serializers.ReadOnlyField()
        # property 는 수정 안됌
        model = models.User

        fields = (
            "username",
            "name",
            "bio",
            "profile_image",
            "stdntnum",
            "postCount",
            "followersCount",
            "followingCount",
            "images"
        )


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            "id",
            "username",
            "name"
        )

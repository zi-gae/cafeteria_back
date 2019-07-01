from rest_framework import serializers
from . import models
from instar.users import models as user_models


class SmallImageSerializer(serializers.ModelSerializer):
    # notification for serializer
    class Meta:
        model = models.Image
        fields = (
            "file",
        )


class UserProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = (
            "id",
            "file",
            "like_count",
            "comment_count"
        )


class FeedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_models.User
        fields = (
            "username",
            "profile_image"
        )


class CommentSerializer(serializers.ModelSerializer):

    creator = FeedUserSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = (
            "id",
            "message",
            "creator"
        )


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Like
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    # foreign key 의 정보를 가져옴
    comments = CommentSerializer(many=True)
    creator = FeedUserSerializer()

    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'content',
            'creator',
            'comments',
            'like_count',
            'created_at',
            'updated_at'
        )

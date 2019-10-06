from rest_framework import serializers
from . import models
from cafeteria.users import models as user_models


class SmallImageSerializer(serializers.ModelSerializer):
    # notification for serializer
    class Meta:
        model = models.Image
        fields = (
            "file",
        )


class UserProfileImageSerializer(serializers.ModelSerializer):
    # user profile for serializer
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
            "creator",
            "referComment",
            'natural_time',
            'updated_at'
        )


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Like
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    # foreign key 의 정보를 가져옴
    comments = CommentSerializer(many=True)
    creator = FeedUserSerializer()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = models.Image
        fields = (
            'id',
            'title',
            'file',
            'content',
            'creator',
            'comments',
            'like_count',
            'comment_count',
            'natural_time',
            'updated_at',
            'is_liked'
        )

    def get_is_liked(self, obj):
        if 'request' in self.context:
            request = self.context['request']
            print("context: ", self.context)

            try:
                models.Like.objects.get(creator__id=request.user.id, image__id=obj.id)
                return True
            except models.Like.DoesNotExist:
                return False
        return False


class InputImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = (
            'title',
            'file',
            'content',
        )

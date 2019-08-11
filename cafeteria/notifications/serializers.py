from rest_framework import serializers
from . import models
from cafeteria.users import serializers as user_serializers
from cafeteria.images import serializers as image_serializers


class NotificationsSerializers(serializers.ModelSerializer):

    creator = user_serializers.ListUserSerializer(read_only=True)
    image = image_serializers.SmallImageSerializer(read_only=True)

    class Meta:
        model = models.Notification
        fields = (
            "creator",
            "to",
            "notification_type",
            "image"
        )

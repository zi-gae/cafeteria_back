from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers


class Notifications(APIView):

    # 알림 리스트
    def get(self, request, format=None):

        user = request.user

        notifications = models.Notification.objects.filter(to=user)

        serializer = serializers.NotificationsSerializers(notifications, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# 알림 생성
def createNotification(creator, to, notification_type, image=None, comment=None):

    notification = models.Notification.objects.create(
        creator=creator,
        to=to,
        notification_type=notification_type,
        image=image,
        comment=comment
    )
    notification.save()

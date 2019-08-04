from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from instar.notifications import views as notification_view


class ExploreUser(APIView):

    def get(self, request, format=None):

        lastFive = models.User.objects.all().order_by('-date_joined')[:5]
        serializer = serializers.ListUserSerializer(Fve, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FollowUser(APIView):

    def post(self, request, user_id, format=None):

        user = request.user

        try:
            userToFollow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        create_notification = notification_view.create_notification(user, userToFollow, "follow")

        user.following.add(userToFollow)
        userToFollow.followers.add(user)

        user.save()
        userToFollow.save()

        return Response(status=status.HTTP_200_OK)


class UnFollowUser(APIView):

    def post(self, request, user_id, format=None):

        user = request.user

        try:
            userToFollow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.remove(userToFollow)
        userToFollow.followers.remove(user)

        user.save()
        userToFollow.save()

        return Response(status=status.HTTP_200_OK)


class UserProfile(APIView):

    def get(self, request, username, format=None):

        try:
            foundUser = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserProfileSerializer(foundUser)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

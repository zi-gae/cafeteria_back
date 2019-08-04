from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from instar.notifications import views as notification_view


class ExploreUser(APIView):

    def get(self, request, format=None):

        lastFive = models.User.objects.all().order_by('-date_joined')[:5]
        serializer = serializers.ListUserSerializer(lastFive, many=True)

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

    def getUser(self, username):
        try:
            foundUser = models.User.objects.get(username=username)
            return foundUser
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, username, format=None):

        foundUser = self.getUser(username)

        serializer = serializers.UserProfileSerializer(foundUser)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username, format=None):
        user = request.user
        foundUser = self.getUser(username)

        if user == foundUser:
            serializer = serializers.UserProfileSerializer(foundUser, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data,  status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.error, status=status.HTTP_400_BAD_REQUEST)

        elif user != foundUser:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

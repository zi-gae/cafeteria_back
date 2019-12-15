from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from cafeteria.notifications import views as notification_view
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
import requests
import json


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

    # 유저 프로필 보기
    def get(self, request, username, format=None):
        foundUser = self.getUser(username)

        serializer = serializers.UserProfileSerializer(foundUser, context={"request": request})

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # 유저 프로필 수정
    def put(self, request, username, format=None):
        user = request.user
        foundUser = self.getUser(username)
        if("profile_image" in request.data):
            if(request.data["profile_image"] == 'null'):
                data = {'profile_image': None}
            else:
                data = request.data
        else:
            data = request.data
        if user == foundUser:
            serializer = serializers.UserProfileSerializer(
                foundUser, data=data, partial=True, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data,  status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.error, status=status.HTTP_400_BAD_REQUEST)

        elif user != foundUser:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ChangePassword(APIView):

    # 패스워드 변경
    def put(self, request, username, format=None):
        user = request.user
        if user.username == username:
            currentPassword = request.data.get('currentPassword', None)
            match = user.check_password(currentPassword)
            if match and currentPassword is not None:
                newPassword = request.data.get('newPassword', None)
                if newPassword is not None:
                    user.set_password(newPassword)
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter


class PushToken(APIView):

    def getUser(self, username):
        try:
            foundUser = models.User.objects.get(username=username)
            return foundUser
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        username = request.user
        foundUser = self.getUser(username)
        serializer = serializers.UserPushToken(data=request.data)
        if username == foundUser:
            serializer = serializers.UserProfileSerializer(
                foundUser, data=request.data, partial=True, allow_null=True, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data,  status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.error, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=serializer.error, status=status.HTTP_400_BAD_REQUEST)


class IsAlreadyId(APIView):

    def get(self, request, username, format=None):
        try:
            foundID = models.User.objects.get(username=username)
            return Response(status=status.HTTP_302_FOUND)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_202_ACCEPTED)


class IsAlreadyName(APIView):

    def get(self, request, name, format=None):
        try:
            foundNickname = models.User.objects.get(name=name)
            return Response(status=status.HTTP_302_FOUND)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_202_ACCEPTED)


class IsAlreadyEmail(APIView):

    def get(self, request, email, format=None):
        try:
            foundEmail = models.User.objects.get(email=email)
            return Response(status=status.HTTP_302_FOUND)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_202_ACCEPTED)


class StudentAuthentication(APIView):

    def getUser(self, username):
        try:
            foundUser = models.User.objects.get(username=username)
            return foundUser
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, format=None):
        username = request.user
        foundUser = self.getUser(username)
        if username == foundUser:
            serializer = serializers.UserAuthentication(
                foundUser, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data,  status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.error, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=serializer.error, status=status.HTTP_400_BAD_REQUEST)

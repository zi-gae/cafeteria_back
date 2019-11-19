from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers
from cafeteria.notifications import views as notificationView
from cafeteria.users import models as user_models
from cafeteria.users import serializers as userSerializers
from django.db.models import Q
import requests
import json


class Images(APIView):

    def get(self, request, format=None):
        user = request.user
        try:
            user_models.User.objects.get(id=user.id)
        except user_models.User.DoesNotExist:
            return Response(data=serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        allImages = models.Image.objects.all().order_by('-created_at')
        serializer = serializers.ImageSerializer(allImages, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        user = request.user
        try:
            user_models.User.objects.get(id=user.id)
        except user_models.User.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = serializers.ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 좋아요 url 눌렀을때 view
class LikeImage(APIView):

    # 좋아요 리스트
    def get(self, request, post_id, format=None):
        like = models.Like.objects.filter(image__id=post_id)
        likeCreatorIds = like.values('creator_id')
        users = user_models.User.objects.filter(id__in=likeCreatorIds)
        # id__in => id 는 기본적으로 가지고 있고 __in => 주어진 리스트안에 존재하는 자료 검색
        serializer = userSerializers.ListUserSerializer(users, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # 좋아요 생성
    def post(self, request, post_id, format=None):
        user = request.user
        try:
            foundImage = models.Image.objects.get(id=post_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preExistingLike = models.Like.objects.get(
                creator=user,
                image=foundImage
            )
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        except models.Like.DoesNotExist:
            new_like = models.Like.objects.create(
                creator=user,
                image=foundImage
            )
            new_like.save()
            if user.id != foundImage.creator.id:
                if(str(type(foundImage.creator.push_token)) == "<class 'str'>"):
                    payload = {
                        "to": foundImage.creator.push_token,
                        "title": "알림",
                        "sound": "default",
                        "body": "회원님의 게시글을 좋아합니다."
                    }
                    url = "https://exp.host/--/api/v2/push/send"
                    header = {
                        "Content-Type": "application/json",
                    }
                    requests.post(url, data=json.dumps(payload), headers=header)
                else:
                    print("push_token:", foundImage.creator.push_token)
                createNotification = notificationView.createNotification(
                    user, foundImage.creator, "like", foundImage)
            return Response(status=status.HTTP_201_CREATED)


# 좋아요 취소
class UnLikeImage(APIView):
    def delete(self, request, post_id, format=None):
        user = request.user
        try:
            foundImage = models.Image.objects.get(id=post_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preExistingLike = models.Like.objects.get(
                creator=user,
                image=foundImage
            )
            preExistingLike.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except models.Like.DoesNotExist:
            return Response(status=status.HTTP_201_CREATED)


# 게시글 댓글 달기
class CommentOnImage(APIView):

    def post(self, request, post_id, format=None):
        try:
            foundImage = models.Image.objects.get(id=post_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CommentSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            serializer.save(creator=user, image=foundImage)
            if user.id != foundImage.creator.id:
                if(str(type(foundImage.creator.push_token)) == "<class 'str'>"):
                    payload = {
                        "to": foundImage.creator.push_token,
                        "title": "알림",
                        "sound": "default",
                        "body": "회원님의 게시글에 새로운 댓글이 달렸어요."
                    }
                    url = "https://exp.host/--/api/v2/push/send"
                    header = {
                        "Content-Type": "application/json",
                    }
                    requests.post(url, data=json.dumps(payload), headers=header)

                notification = notificationView.createNotification(
                    user, foundImage.creator, "comment", foundImage, serializer.data["message"])
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 대댓글
class CommentOnComment(APIView):
    def post(self, request, post_id, comment_id, format=None):
        try:
            foundImage = models.Image.objects.get(id=post_id)
            foundComment = models.Comment.objects.get(id=comment_id)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CommentSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            if(user != foundComment.creator.username):
                payload = {
                    "to": foundComment.creator.push_token,
                    "title": "알림",
                    "sound": "default",
                    "body": "회원님의 댓글에 새로운 대댓글이 달렸어요."
                }
                url = "https://exp.host/--/api/v2/push/send"
                header = {
                    "Content-Type": "application/json",
                }
                requests.post(url, data=json.dumps(payload), headers=header)

            serializer.save(creator=user, image=foundImage)
            if user.id != foundImage.creator.id:
                notification = notificationView.createNotification(
                    user, foundComment.creator, "on_comment", foundImage, serializer.data["message"])
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 게시글 나의 댓글 삭제
class Comment(APIView):
    def delete(self, request, comment_id, format=None):
        user = request.user
        try:
            foundComment = models.Comment.objects.get(id=comment_id, creator=user)
            foundComment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# 내 게시글에 달린 댓글 삭제
class ModerateComment(APIView):

    def delete(self, request, post_id, comment_id, format=None):
        try:
            user = request.user
            foundComment = models.Comment.objects.get(id=comment_id, image__id=post_id, image__creator=user)
            foundComment.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)


class TitleSearch(APIView):

    def get(self, request, format=None):

        try:
            search = request.query_params.get("title", None)
            # get 으로 넘어오는 값이 없으면 None

        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        images = models.Image.objects.filter(title__icontains=search).distinct()
        # contains => 포함하는 결과를 찾음
        # icontains => 대소문자 구분 안함
        # exact => === 하는걸 찾음
        # distinct => distinct 2개 이상 키워드로 검색 했을때 결과 중복 제거
        serializer = serializers.ImageSerializer(images, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


# 내용 검색
class ContentSearch(APIView):

    def get(self, request, format=None):

        search = request.query_params.get("content", None)

        if search is not None:
            images = models.Image.objects.filter(content__icontains=search).distinct()
            serializer = serializers.ImageSerializer(images, many=True, context={'request': request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# 내용 제목 검색
class ContentTitleSearch(APIView):

    def get(self, request, format=None):

        search = request.query_params.get("total", None)

        if search is not None:
            images = models.Image.objects.filter(Q(title__icontains=search) | Q(content__icontains=search)).distinct()
            serializer = serializers.ImageSerializer(images, many=True, context={'request': request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# 이미지 디테일
class ImageDetail(APIView):

    # 게시글 존재 여부 확인
    def findOwnImage(self, post_id, user):
        try:
            image = models.Image.objects.get(id=post_id, creator=user)
            return image
        except models.Image.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

    # 게시글 상세 보기
    def get(self, request, post_id, format=None):

        user = request.user

        try:
            image = models.Image.objects.get(id=post_id)
        except models.Image.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

        serializer = serializers.ImageSerializer(image, context={'request': request})
        return Response(serializer.data)

    # 게시글 수정
    def put(self, request, post_id, format=None):
        user = request.user
        image = self.findOwnImage(post_id, user)
        serializer = serializers.InputImageSerializer(image, data=request.data, partial=True)
        # partial => update 할때 require=True 이면 기존의 값을 이어 받음
        # require 속성이 True 이고 값을 입력하지 않을때 partial 속성을 주지 않으면 serializer 가 제대로 동작 하지 않음
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 게시글 삭제
    def delete(self, request, post_id, format=None):

        user = request.user
        image = self.findOwnImage(post_id, user)

        if image is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

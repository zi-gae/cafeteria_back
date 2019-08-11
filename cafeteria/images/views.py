from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers
from cafeteria.notifications import views as notificationView
from cafeteria.users import models as user_models
from cafeteria.users import serializers as userSerializers


class Feed(APIView):

    def get(self, request, format=None):
        user = request.user
        try:
            user_models.User.objects.get(id=user.id)
        except user_models.User.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        allImages = models.Image.objects.all().order_by('-created_at')
        serializer = serializers.ImageSerializer(allImages, many=True)
        return Response(serializer.data)


# 좋아요 url 눌렀을때 view
class LikeImage(APIView):

    def get(self, request, image_id, format=None):

        like = models.Like.objects.filter(image__id=image_id)
        likeCreatorIds = like.values('creator_id')
        users = user_models.User.objects.filter(id__in=likeCreatorIds)
        # id__in => id 는 기본적으로 가지고 있고 __in => 주어진 리스트안에 존재하는 자료 검색

        serializer = userSerializers.ListUserSerializer(users, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, image_id, format=None):

        user = request.user
        try:
            foundImage = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preExistingLike = models.Like.objects.get(
                creator=user,
                image=foundImage
            )
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        except models.Like.DoesNotExist:

            createNotification = notificationView.createNotification(user, foundImage.creator, "like", foundImage)
            new_like = models.Like.objects.create(
                creator=user,
                image=foundImage
            )
            new_like.save()

            return Response(status=status.HTTP_201_CREATED)


# 좋아요 취소
class UnLikeImage(APIView):
    def delete(self, request, image_id, format=None):
        user = request.user
        try:
            foundImage = models.Image.objects.get(id=image_id)
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


# 이미지에 댓글 달기
class CommentOnImage(APIView):

    def post(self, request, image_id, format=None):

        try:
            foundImage = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CommentSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            serializer.save(creator=user, image=foundImage)
            notification = notificationView.createNotification(
                user, foundImage.creator, "comment", foundImage, serializer.data["message"])
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 이미지에 댓글 삭제
class Comment(APIView):

    def delete(self, request, comment_id, format=None):
        user = request.user
        try:
            foundComment = models.Comment.objects.get(id=comment_id, creator=user)
            foundComment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# 내 게시글에 달린 댓글 삭제
class ModerateComment(APIView):

    def delete(self, request, image_id, comment_id, format=None):
        try:
            user = request.user
            foundComment = models.Comment.objects.get(id=comment_id, image__id=image_id, image__creator=user)
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
        serializer = serializers.ImageSerializer(images, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


# 내용 검색
class ContentSearch(APIView):

    def get(self, request, format=None):

        search = request.query_params.get("content", None)

        if search is not None:
            images = models.Image.objects.filter(content__icontains=search).distinct()
            serializer = serializers.ImageSerializer(images, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# 이미지 디테일
class ImageDetail(APIView):

    def findOwnImage(self, image_id, user):
        try:
            image = models.Image.objects.get(id=image_id, creator=user)
            return image
        except models.Image.DoesNotExist:
            return None

    def get(self, request, image_id, format=None):

        user = request.user

        try:
            image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

        serializer = serializers.ImageSerializer(image)
        return Response(serializer.data)

    def put(self, request, image_id, format=None):

        user = request.user

        image = self.findOwnImage(image_id, user)

        serializer = serializers.InputImageSerializer(image, data=request.data, partial=True)
        # partial => update 할때 require=True 이면 기존의 값을 이어 받음
        # require 속성이 True 이고 값을 입력하지 않을때 partial 속성을 주지 않으면 serializer 가 제대로 동작 하지 않음
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, image_id, format=None):

        user = request.user
        image = self.findOwnImage(image_id, user)

        if image is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

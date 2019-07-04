from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers
from instar.notifications import views as notification_view


class Feed(APIView):

    def get(self, request, format=None):
        user = request.user
        following_users = user.following.all()
        image_list = []
        sorted_list = []
        for following_user in following_users:
            user_images = following_user.images.all()[:5]
            for image in user_images:
                image_list.append(image)

        sorted_list = sorted(image_list, key=lambda image: image.created_at, reverse=True)
        serializer = serializers.ImageSerializer(sorted_list, many=True)
        return Response(serializer.data)


# 좋아요 url 눌렀을때 view
class LikeImage(APIView):

    def post(self, request, image_id, format=None):

        user = request.user
        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            pre_existing_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        except models.Like.DoesNotExist:

            create_notification = notification_view.create_notification(user, found_image.creator, "like", found_image)
            new_like = models.Like.objects.create(
                creator=user,
                image=found_image
            )
            new_like.save()

            return Response(status=status.HTTP_201_CREATED)


# 좋아요 취소
class UnLikeImage(APIView):
    def delete(self, request, image_id, format=None):
        user = request.user
        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            pre_existing_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )
            pre_existing_like.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except models.Like.DoesNotExist:
            return Response(status=status.HTTP_201_CREATED)


# 이미지에 댓글 달기
class CommentOnImage(APIView):

    def post(self, request, image_id, format=None):

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CommentSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            serializer.save(creator=user, image=found_image)
            notification = notification_view.create_notification(
                user, found_image.creator, "comment", found_image, serializer.data["message"])
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 이미지에 댓글 삭제
class Comment(APIView):

    def delete(self, request, comment_id, format=None):
        user = request.user
        try:
            found_comment = models.Comment.objects.get(id=comment_id, creator=user)
            found_comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# todo list
# 1.게시글에 달린 댓글 삭제 (작성자)
#

# 타이틀 검색
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

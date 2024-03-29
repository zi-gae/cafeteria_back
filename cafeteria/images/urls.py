from django.urls import path
from . import views

app_name = "posts"
urlpatterns = [
    path("", views.Images.as_view(), name="feed"),
    path("<int:post_id>/", views.ImageDetail.as_view(), name="feed"),
    path("<int:post_id>/report/", views.CrimeReport.as_view(), name="crime_report"),
    path("<int:post_id>/like/", views.LikeImage.as_view(), name="like_image"),
    path("<int:post_id>/unlike/", views.UnLikeImage.as_view(), name="unlike_image"),
    path("<int:post_id>/comments/", views.CommentOnImage.as_view(), name="comment_image"),
    path("<int:post_id>/<int:comment_id>/comments/", views.CommentOnComment.as_view(), name="comment_on_comment"),
    path("<int:post_id>/comments/<int:comment_id>", views.ModerateComment.as_view(), name="comment_image"),
    path("comments/<int:comment_id>/", views.Comment.as_view(), name="comment_delete"),
    path("title_search/", views.TitleSearch.as_view(), name="title_search"),
    path("content_search/", views.ContentSearch.as_view(), name="content_search"),
    path("total_search/", views.ContentTitleSearch.as_view(), name="total_search")
]

# my image on comment delete

# 3/comment/5
# image-id: 3
# delete commentId: 5


# step0 url view 만들기
# step2 url 에서 아이디 가져오기
# step3 해당 id 의 이미지 찾고
# step4 좋아요 생성

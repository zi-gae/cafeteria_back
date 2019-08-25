from django.urls import path
from . import views


app_name = "users"
urlpatterns = [
    path("explore/", view=views.ExploreUser.as_view(), name="explore_user"),
    path("<int:user_id>/follow/", view=views.FollowUser.as_view(), name="flw_user"),
    path("<int:user_id>/unfollow/", view=views.UnFollowUser.as_view(), name="uflw_user"),
    path("<username>/", view=views.UserProfile.as_view(), name="user_propfile"),
    path("<username>/password/", view=views.ChangePassword.as_view(), name="password"),
    path("login/kakao/", view=views.KakaoLogin.as_view(), name='kakao_login')

]

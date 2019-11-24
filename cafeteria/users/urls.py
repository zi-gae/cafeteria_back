from django.urls import path
from . import views


app_name = "users"
urlpatterns = [
    path("push-token/", view=views.PushToken.as_view(), name='push_token'),
    path("authentication/", view=views.StudentAuthentication.as_view(), name='authentication'),
    path("explore/", view=views.ExploreUser.as_view(), name="explore_user"),
    path("<int:user_id>/follow/", view=views.FollowUser.as_view(), name="flw_user"),
    path("<int:user_id>/unfollow/", view=views.UnFollowUser.as_view(), name="uflw_user"),
    path("<username>/password/", view=views.ChangePassword.as_view(), name="password"),
    path("<username>/", view=views.UserProfile.as_view(), name="user_propfile"),
    path("login/kakao/", view=views.KakaoLogin.as_view(), name='kakao_login'),
    path("<name>/already_nickname/", view=views.IsAlreadyName.as_view(), name='is_already_name'),
    path("<email>/already_email/", view=views.IsAlreadyEmail.as_view(), name='is_already_email'),
    path("<username>/already_id/", view=views.IsAlreadyId.as_view(), name='is_already_id'),
]

from rest_framework import serializers
from . import models
from cafeteria.images import serializers as image_serialiazers
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=100,
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    stdntnum = serializers.IntegerField(write_only=True)
    name = serializers.CharField(
        max_length=100,
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    
    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    ("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'stdntnum': self.validated_data.get('stdntnum',''),
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'name': self.validated_data.get('name', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class UserProfileSerializer(serializers.ModelSerializer):

    images = image_serialiazers.UserProfileImageSerializer(many=True)

    class Meta:
        # postCount = serializers.ReadOnlyField()
        # followersCount = serializers.ReadOnlyField()
        # followingCount = serializers.ReadOnlyField()
        # property 는 수정 안됌
        model = models.User

        fields = (
            "username",
            "name",
            "bio",
            "profile_image",
            "stdntnum",
            "postCount",
            "followersCount",
            "followingCount",
            "images"
        )


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            "id",
            "username",
            "name"
        )

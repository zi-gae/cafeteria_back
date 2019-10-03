from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class CustomUserAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_field
        user = super().save_user(request, user, form, False)
        user_field(user, 'stdntnum', request.data.get('stdntnum', ''))
        user_field(user, 'email', request.data.get('email', ''))
        user_field(user, 'name', request.data.get('name',''))
        user.save()
        return user

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

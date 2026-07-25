from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .models import UserProfile


class CapitalAutosSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Use provider data to create a useful standard Django user profile."""

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.first_name = data.get("first_name") or user.first_name
        user.last_name = data.get("last_name") or user.last_name
        if not user.first_name and data.get("name"):
            user.first_name, _, user.last_name = data["name"].partition(" ")
        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        picture = sociallogin.account.extra_data.get("picture", "")
        if isinstance(picture, dict):
            picture = picture.get("data", {}).get("url", "")
        profile, _ = UserProfile.objects.get_or_create(user=user)
        if picture:
            profile.avatar_url = picture
            profile.save(update_fields=["avatar_url"])
        return user

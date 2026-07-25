from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    """Optional customer details collected from social-login providers."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    avatar_url = models.URLField(blank=True)

    def __str__(self):
        return f"Profile for {self.user.get_username()}"

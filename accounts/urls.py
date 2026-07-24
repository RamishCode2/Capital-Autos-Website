from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    # Backwards-compatible account-prefixed login URL.  The public login URL
    # is /login/ in the project URLconf.
    path("login/", views.user_login, name="accounts_login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.profile, name="profile"),
]

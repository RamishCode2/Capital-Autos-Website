"""
URL configuration for CA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from core.views import home
from accounts import views as account_views

urlpatterns = [
    path(
    "password-reset/",
    account_views.CustomPasswordResetView.as_view(),
    name="password_reset",
),

path(
    "password-reset/done/",
    account_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"
    ),
    name="password_reset_done",
),

path(
    "reset/<uidb64>/<token>/",
    account_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html"
    ),
    name="password_reset_confirm",
),

path(
    "reset/done/",
    account_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"
    ),
    name="password_reset_complete",
),
    path("login/", account_views.user_login, name="login"),
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("brands/", include("brands.urls")),
    path("products/", include("products.urls")),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
    path("accounts/", include("accounts.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

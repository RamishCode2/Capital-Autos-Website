from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class PasswordResetFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="buyer", email="buyer@example.com", password="OldPassword123"
        )

    def test_reset_request_does_not_disclose_account_existence(self):
        response = self.client.post(reverse("password_reset"), {"email": "missing@example.com"})
        self.assertRedirects(response, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 0)

    def test_reset_email_uses_secure_django_link(self):
        response = self.client.post(reverse("password_reset"), {"email": self.user.email})
        self.assertRedirects(response, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Reset Your Password")
        self.assertIn("/reset/", mail.outbox[0].body)

    def test_login_accepts_email_address(self):
        response = self.client.post(
            reverse("login"), {"email": self.user.email, "password": "OldPassword123"}
        )
        self.assertEqual(response.status_code, 302)

    def test_login_rejects_external_next_url(self):
        response = self.client.post(
            reverse("login") + "?next=https://example.com/",
            {"email": self.user.email, "password": "OldPassword123"},
        )
        self.assertRedirects(response, reverse("home"))

    def test_logout_requires_post(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.assertRedirects(self.client.post(reverse("logout")), reverse("home"))

    def test_signed_in_navigation_and_profile_pages_render(self):
        self.client.force_login(self.user)
        for route_name in ("home", "profile", "my_orders", "wishlist"):
            with self.subTest(route=route_name):
                self.assertEqual(self.client.get(reverse(route_name)).status_code, 200)

    def test_login_page_renders_without_social_apps(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome back")

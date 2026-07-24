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

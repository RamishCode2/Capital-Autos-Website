from django.test import TestCase
from django.urls import reverse

from .models import NewsletterSubscriber

# Create your tests here.


class NewsletterSubscriptionTests(TestCase):
    def test_newsletter_subscription_validates_and_deduplicates_email(self):
        url = reverse("newsletter_subscribe")
        invalid = self.client.post(url, {"email": "not-an-email"})
        self.assertRedirects(invalid, reverse("home"))
        self.assertEqual(NewsletterSubscriber.objects.count(), 0)

        self.client.post(url, {"email": " SHOPPER@example.com "})
        self.client.post(url, {"email": "shopper@example.com"})
        self.assertEqual(NewsletterSubscriber.objects.count(), 1)

    def test_newsletter_endpoint_requires_post(self):
        self.assertEqual(self.client.get(reverse("newsletter_subscribe")).status_code, 405)

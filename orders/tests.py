from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from brands.models import Brand, CarModel
from products.models import Category, Product
from .models import Order, OrderItem


class CheckoutFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="buyer", email="buyer@example.com", password="TestPassword123!"
        )
        brand = Brand.objects.create(name="Test Motors")
        model = CarModel.objects.create(name="Test Model", brand=brand)
        category = Category.objects.create(name="Test Parts")
        self.product = Product.objects.create(
            brand=brand,
            car_model=model,
            category=category,
            name="Test Filter",
            sku="ORDER-TEST-FILTER-1",
            price=Decimal("100.00"),
            discount_price=Decimal("80.00"),
            stock=3,
            description="A test product",
        )
        self.client.force_login(self.user)
        session = self.client.session
        session["cart"] = {str(self.product.id): 2}
        session.save()

    def test_checkout_creates_order_at_discounted_price_and_decrements_stock(self):
        response = self.client.post(
            reverse("checkout"),
            {
                "full_name": "Test Buyer",
                "email": "buyer@example.com",
                "phone": "123456789",
                "address": "1 Test Street",
                "city": "Test City",
                "postal_code": "12345",
                "payment_method": "COD",
            },
        )
        order = Order.objects.get(user=self.user)
        self.assertRedirects(response, reverse("order_success", args=[order.id]))
        self.assertEqual(order.total_price, Decimal("160.00"))
        item = OrderItem.objects.get(order=order)
        self.assertEqual(item.price, Decimal("80.00"))
        self.assertEqual(item.quantity, 2)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 1)
        self.assertEqual(self.client.session["cart"], {})

    def test_checkout_rejects_quantity_above_current_stock(self):
        self.product.stock = 1
        self.product.save()
        response = self.client.get(reverse("checkout"))
        self.assertRedirects(response, reverse("cart"))
        self.assertFalse(Order.objects.exists())

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from brands.models import Brand, CarModel
from products.models import Category, Product


class CartFlowTests(TestCase):
    def setUp(self):
        brand = Brand.objects.create(name="Test Motors")
        model = CarModel.objects.create(name="Test Model", brand=brand)
        category = Category.objects.create(name="Test Parts")
        self.product = Product.objects.create(
            brand=brand,
            car_model=model,
            category=category,
            name="Test Filter",
            sku="TEST-FILTER-1",
            price=Decimal("100.00"),
            stock=2,
            description="A test product",
        )

    def test_add_to_cart_requires_post_and_respects_stock(self):
        url = reverse("add_to_cart", args=[self.product.id])
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertEqual(self.client.post(url).status_code, 302)
        self.client.post(url)
        self.client.post(url)
        self.assertEqual(self.client.session["cart"][str(self.product.id)], 2)

    def test_cart_removes_stale_products_instead_of_erroring(self):
        session = self.client.session
        session["cart"] = {"999999": 2, "invalid": 1}
        session.save()
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session["cart"], {})

    def test_cart_uses_discount_price(self):
        self.product.discount_price = Decimal("80.00")
        self.product.save()
        session = self.client.session
        session["cart"] = {str(self.product.id): 1}
        session.save()
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total"], Decimal("80.00"))

    def test_invalid_shop_filters_do_not_raise_server_errors(self):
        response = self.client.get("/products/shop/?brand=invalid&category=invalid")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["products"])

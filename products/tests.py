from django.test import TestCase
from django.urls import reverse

from brands.models import Brand, CarModel
from products.models import Category, Product

# Create your tests here.


class WishlistFlowTests(TestCase):
    def setUp(self):
        brand = Brand.objects.create(name="Wishlist Motors")
        model = CarModel.objects.create(name="Wishlist Model", brand=brand)
        category = Category.objects.create(name="Wishlist Parts")
        self.product = Product.objects.create(
            brand=brand,
            car_model=model,
            category=category,
            name="Wishlist Filter",
            sku="WISHLIST-FILTER-1",
            price="25.00",
            stock=1,
            description="A wishlist test product",
        )

    def test_wishlist_toggle_adds_and_removes_product(self):
        toggle_url = reverse("toggle_wishlist", args=[self.product.id])
        self.assertEqual(self.client.get(toggle_url).status_code, 405)
        self.client.post(toggle_url, {"next": reverse("shop")})
        self.assertIn(str(self.product.id), self.client.session["wishlist"])
        response = self.client.get(reverse("wishlist"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.client.post(toggle_url, {"next": reverse("shop")})
        self.assertEqual(self.client.session["wishlist"], [])

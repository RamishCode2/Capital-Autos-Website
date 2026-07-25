from django.db import models
from brands.models import Brand, CarModel
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Product(models.Model):
    STOCK_STATUS = (
        ("in_stock", "In Stock"),
        ("out_of_stock", "Out of Stock"),
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="products"
    )

    car_model = models.ForeignKey(
        CarModel,
        on_delete=models.CASCADE,
        related_name="products"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(default=0)
    stock_status = models.CharField(
        max_length=20,
        choices=STOCK_STATUS,
        default="in_stock"
    )

    image = models.ImageField(upload_to="products/")
    description = models.TextField()

    is_active = models.BooleanField(default=True)
    is_flash_sale = models.BooleanField(
        default=False,
        help_text="Show this product in the homepage Flash Sales section."
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Show this product in Recommended For You."
    )
    is_best_seller = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    badge_label = models.CharField(
        max_length=30,
        blank=True,
        help_text="Optional card badge, for example: Hot, New, or Best Seller."
    )
    homepage_order = models.PositiveIntegerField(
        default=0,
        help_text="Lower numbers appear first in homepage sections."
    )
    average_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0,
        help_text="Optional product rating from 0.0 to 5.0."
    )
    review_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def discount_percentage(self):
        """Return a display-friendly discount without storing duplicate data."""
        if self.discount_price is not None and self.price:
            return round(((self.price - self.discount_price) / self.price) * 100)
        return 0

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="products/gallery/")
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"

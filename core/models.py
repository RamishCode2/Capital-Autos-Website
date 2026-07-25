from django.db import models


class HeroSlide(models.Model):
    eyebrow = models.CharField(max_length=80, blank=True)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=220, blank=True)
    button_label = models.CharField(max_length=40, default="Shop Now")
    button_url = models.CharField(max_length=255, default="/products/shop/")
    background_image = models.ImageField(upload_to="hero_slides/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "id")

    def __str__(self):
        return self.title

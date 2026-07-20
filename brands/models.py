from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CarModel(models.Model):
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="car_models"
    )
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        unique_together = ("brand", "name")

    def __str__(self):
        return f"{self.brand.name} - {self.name}"
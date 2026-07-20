from django.contrib import admin
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "car_model",
        "category",
        "price",
        "stock",
        "stock_status",
        "is_active",
    )

    list_filter = (
        "brand",
        "category",
        "stock_status",
        "is_active",
    )

    search_fields = (
        "name",
        "sku",
    )

    inlines = [ProductImageInline]
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
        "is_flash_sale",
        "is_featured",
        "is_best_seller",
        "is_active",
    )

    list_filter = (
        "brand",
        "category",
        "stock_status",
        "is_flash_sale",
        "is_featured",
        "is_best_seller",
        "is_new",
        "is_active",
    )

    search_fields = (
        "name",
        "sku",
    )

    inlines = [ProductImageInline]
    list_editable = (
        "is_flash_sale",
        "is_featured",
        "is_best_seller",
        "is_active",
    )
    fieldsets = (
        ("Product information", {"fields": ("name", "slug", "sku", "brand", "car_model", "category", "description", "image")}),
        ("Pricing & availability", {"fields": ("price", "discount_price", "stock", "stock_status", "is_active")}),
        ("Homepage placement", {"fields": ("is_flash_sale", "is_featured", "is_best_seller", "is_new", "badge_label", "homepage_order")}),
        ("Customer feedback", {"fields": ("average_rating", "review_count")}),
    )

from django.shortcuts import render
from django.db.models import Q
from brands.models import Brand
from products.models import Category, Product
from .models import HeroSlide


def home(request):
    brands = Brand.objects.all()
    categories = Category.objects.all()[:9]
    active_products = Product.objects.filter(is_active=True).select_related("brand", "category")
    homepage_products = active_products.order_by("homepage_order", "name")
    flash_products = homepage_products.filter(
        Q(is_flash_sale=True) | Q(discount_price__isnull=False)
    ).distinct()[:8]
    recommended_products = homepage_products.filter(
        Q(is_featured=True) | Q(is_best_seller=True) | Q(is_new=True)
    ).distinct()[:12]
    if not recommended_products:
        recommended_products = homepage_products[:12]

    context = {
        "brands": brands,
        "categories": categories,
        "flash_products": flash_products,
        "recommended_products": recommended_products,
        "hero_slides": HeroSlide.objects.filter(is_active=True),
    }

    return render(request, "core/home.html", context)

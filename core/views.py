from django.shortcuts import render
from brands.models import Brand
from products.models import Category, Product


def home(request):
    brands = Brand.objects.all()
    categories = Category.objects.all()[:8]
    featured_products = Product.objects.filter(is_active=True)[:8]

    context = {
        "brands": brands,
        "categories": categories,
        "featured_products": featured_products,
    }

    return render(request, "home.html", context)
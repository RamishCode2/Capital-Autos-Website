from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from brands.models import CarModel
from .models import Category, Product



def category_list(request, model_id):
    car_model = get_object_or_404(CarModel, id=model_id)

    categories = Category.objects.filter(
        products__car_model=car_model
    ).distinct().order_by("name")

    context = {
        "car_model": car_model,
        "categories": categories,
    }

    return render(request, "products/category_list.html", context)


def product_list(request, model_id, category_id):

    car_model = get_object_or_404(CarModel, id=model_id)

    category = get_object_or_404(Category, id=category_id)

    products = Product.objects.filter(
        car_model=car_model,
        category=category,
        is_active=True
    ).order_by("name")

    context = {
        "car_model": car_model,
        "category": category,
        "products": products,
    }

    return render(request, "products/product_list.html", context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    context = {
        "product": product,
        "related_products": related_products,
    }

    return render(request, "products/product_detail.html", context)

def search_products(request):

    query = request.GET.get("q")

    products = []

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(car_model__name__icontains=query) |
            Q(car_model__brand__name__icontains=query)
        ).distinct()

    context = {
        "query": query,
        "products": products,
    }

    return render(request, "products/search_results.html", context)
from brands.models import Brand


def shop(request):

    products = Product.objects.filter(is_active=True)

    brand = request.GET.get("brand")
    category = request.GET.get("category")

    if brand:
        products = products.filter(car_model__brand_id=brand)

    if category:
        products = products.filter(category_id=category)

    context = {
        "products": products.order_by("name"),
        "brands": Brand.objects.all(),
        "categories": Category.objects.all(),
    }

    return render(request, "products/shop.html", context)
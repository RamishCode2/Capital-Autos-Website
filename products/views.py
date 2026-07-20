from django.shortcuts import render, get_object_or_404
from brands.models import CarModel
from .models import Product


def product_list(request, model_id):
    car_model = get_object_or_404(CarModel, id=model_id)
    products = Product.objects.filter(car_model=car_model).order_by("name")

    context = {
        "car_model": car_model,
        "products": products,
    }

    return render(request, "products/product.html", context)


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
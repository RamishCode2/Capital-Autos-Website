from django.shortcuts import render, get_object_or_404
from brands.models import CarModel
from .models import Product


def product_list(request, model_id):
    car_model = get_object_or_404(CarModel, id=model_id)

    products = Product.objects.filter(
        car_model=car_model,
        is_active=True
    )

    context = {
        "car_model": car_model,
        "products": products,
    }

    return render(request, "products/product_list.html", context)
from django.shortcuts import render, get_object_or_404
from .models import Brand


def brand_detail(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    car_models = brand.car_models.all()

    context = {
        "brand": brand,
        "car_models": car_models,
    }

    return render(request, "brands/brand_detail.html", context)
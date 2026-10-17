from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Brand


def brand_detail(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    car_models = brand.car_models.all()

    context = {
        "brand": brand,
        "car_models": car_models,
    }

    return render(request, "brands/brand_detail.html", context)


def brand_directory(request):
    brands = Brand.objects.all().annotate(product_count=Count("products", distinct=True))
    return render(request, "brands/brand.html", {"brands": brands})

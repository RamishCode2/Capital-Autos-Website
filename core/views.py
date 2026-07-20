from django.shortcuts import render
from brands.models import Brand


def home(request):
    brands = Brand.objects.all()

    context = {
        "brands": brands
    }

    return render(request, "home.html", context)
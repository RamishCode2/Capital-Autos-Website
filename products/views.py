from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from brands.models import CarModel
from .models import Category, Product



def category_list(request, model_id):
    car_model = get_object_or_404(CarModel, id=model_id)

    categories = Category.objects.filter(
        products__car_model=car_model,
        products__is_active=True,
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
    product = get_object_or_404(Product, id=product_id, is_active=True)

    related_products = Product.objects.filter(
        category=product.category,
        is_active=True,
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
            is_active=True
        ).filter(
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
        try:
            products = products.filter(car_model__brand_id=int(brand))
        except (TypeError, ValueError):
            products = products.none()

    if category:
        try:
            products = products.filter(category_id=int(category))
        except (TypeError, ValueError):
            products = products.none()

    context = {
        "products": products.order_by("name"),
        "brands": Brand.objects.all(),
        "categories": Category.objects.all(),
    }

    return render(request, "products/shop.html", context)


def wishlist(request):
    saved_ids = request.session.get("wishlist", [])
    if not isinstance(saved_ids, list):
        saved_ids = []
    valid_ids = []
    for product_id in saved_ids:
        try:
            valid_ids.append(int(product_id))
        except (TypeError, ValueError):
            continue
    request.session["wishlist"] = valid_ids
    products = Product.objects.filter(id__in=valid_ids, is_active=True).select_related(
        "brand", "category", "car_model"
    )
    return render(request, "products/wishlist.html", {"products": products})


@require_POST
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    saved_ids = request.session.get("wishlist", [])
    if not isinstance(saved_ids, list):
        saved_ids = []
    saved_ids = [str(saved_id) for saved_id in saved_ids if str(saved_id).isdigit()]
    product_key = str(product.id)
    if product_key in saved_ids:
        saved_ids.remove(product_key)
        messages.info(request, f"{product.name} was removed from your wishlist.")
    else:
        saved_ids.append(product_key)
        messages.success(request, f"{product.name} was saved to your wishlist.")
    request.session["wishlist"] = saved_ids

    next_url = request.POST.get("next", "")
    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect("wishlist")

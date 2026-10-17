from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product


def _clean_cart(request):
    """Return a session cart with valid product IDs and positive quantities."""
    raw_cart = request.session.get("cart", {})
    cart = {}
    if isinstance(raw_cart, dict):
        for product_id, quantity in raw_cart.items():
            try:
                clean_id = str(int(product_id))
                clean_quantity = int(quantity)
            except (TypeError, ValueError):
                continue
            if clean_quantity > 0:
                cart[clean_id] = clean_quantity
    if cart != raw_cart:
        request.session["cart"] = cart
    return cart


def _available_product(product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    if product.stock <= 0 or product.stock_status != "in_stock":
        return None
    return product


def _price(product):
    return product.discount_price if product.discount_price is not None else product.price


def cart_detail(request):
    cart = _clean_cart(request)
    items = []
    total = Decimal("0.00")
    changed = False

    for product_id, quantity in list(cart.items()):
        product = Product.objects.filter(id=product_id, is_active=True).first()
        if product is None or product.stock <= 0 or product.stock_status != "in_stock":
            del cart[product_id]
            changed = True
            continue
        if quantity > product.stock:
            quantity = product.stock
            cart[product_id] = quantity
            changed = True
            messages.info(request, f"The quantity for {product.name} was adjusted to available stock.")
        unit_price = _price(product)
        subtotal = unit_price * quantity
        total += subtotal
        items.append({"product": product, "quantity": quantity, "unit_price": unit_price, "subtotal": subtotal})

    if changed:
        request.session["cart"] = cart
    return render(request, "cart/cart.html", {"items": items, "total": total})


@require_POST
def add_to_cart(request, product_id):
    product = _available_product(product_id)
    if product is None:
        messages.error(request, "This product is currently out of stock.")
        return redirect("product_detail", product_id=product_id)

    cart = _clean_cart(request)
    product_key = str(product.id)
    quantity = cart.get(product_key, 0)
    if quantity >= product.stock:
        messages.info(request, f"Only {product.stock} of {product.name} are available.")
    else:
        cart[product_key] = quantity + 1
        request.session["cart"] = cart
        messages.success(request, f"{product.name} was added to your cart.")

    if request.POST.get("buy_now"):
        return redirect("checkout")
    return redirect("cart")


@require_POST
def remove_from_cart(request, product_id):
    cart = _clean_cart(request)
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    return redirect("cart")


@require_POST
def increase_quantity(request, product_id):
    product = Product.objects.filter(id=product_id, is_active=True).first()
    cart = _clean_cart(request)
    product_key = str(product_id)
    if product is None or product.stock <= 0 or product.stock_status != "in_stock":
        cart.pop(product_key, None)
        messages.error(request, "This product is no longer available.")
    elif cart.get(product_key, 0) >= product.stock:
        messages.info(request, f"Only {product.stock} of {product.name} are available.")
    elif product_key in cart:
        cart[product_key] += 1
    request.session["cart"] = cart
    return redirect("cart")


@require_POST
def decrease_quantity(request, product_id):
    cart = _clean_cart(request)
    product_key = str(product_id)
    if product_key in cart:
        if cart[product_key] > 1:
            cart[product_key] -= 1
        else:
            del cart[product_key]
    request.session["cart"] = cart
    return redirect("cart")

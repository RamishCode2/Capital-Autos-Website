from decimal import Decimal
from uuid import uuid4

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product
from .forms import CheckoutForm
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart = request.session.get("cart", {})

    if not isinstance(cart, dict):
        cart = {}
    clean_cart = {}
    for product_id, quantity in cart.items():
        try:
            product_id = str(int(product_id))
            quantity = int(quantity)
        except (TypeError, ValueError):
            continue
        if quantity > 0:
            clean_cart[product_id] = quantity
    if clean_cart != cart:
        request.session["cart"] = clean_cart
    cart = clean_cart

    if not cart:
        return redirect("cart")

    items = []
    total = Decimal("0.00")

    for product_id, quantity in cart.items():
        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            quantity = 0
        product = Product.objects.filter(id=product_id, is_active=True).first()
        if product is None or quantity <= 0 or product.stock < quantity or product.stock_status != "in_stock":
            messages.error(request, "Your cart has an unavailable item or quantity. Please review it before checkout.")
            return redirect("cart")

        unit_price = product.discount_price if product.discount_price is not None else product.price
        subtotal = unit_price * quantity
        total += subtotal
        items.append({"product": product, "quantity": quantity, "unit_price": unit_price, "subtotal": subtotal})

    if request.method == "POST":

        form = CheckoutForm(request.POST)

        if form.is_valid():

            with transaction.atomic():
                locked_products = {
                    str(product.id): product
                    for product in Product.objects.select_for_update().filter(
                        id__in=cart.keys(), is_active=True
                    )
                }
                if any(
                    str(item["product"].id) not in locked_products
                    or locked_products[str(item["product"].id)].stock < item["quantity"]
                    or locked_products[str(item["product"].id)].stock_status != "in_stock"
                    for item in items
                ):
                    messages.error(request, "Stock changed while you were checking out. Please review your cart.")
                    return redirect("cart")

                total = Decimal("0.00")
                order = form.save(commit=False)
                order.user = request.user
                order.order_number = f"CA-{uuid4().hex[:8].upper()}"
                for item in items:
                    product = locked_products[str(item["product"].id)]
                    unit_price = product.discount_price if product.discount_price is not None else product.price
                    item["unit_price"] = unit_price
                    item["subtotal"] = unit_price * item["quantity"]
                    total += item["subtotal"]
                order.total_price = total
                order.save()

                for item in items:
                    product = locked_products[str(item["product"].id)]
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item["quantity"],
                        price=item["unit_price"],
                    )
                    product.stock -= item["quantity"]
                    if product.stock == 0:
                        product.stock_status = "out_of_stock"
                    product.save(update_fields=["stock", "stock_status"])

            request.session["cart"] = {}
            messages.success(request, "Your order has been placed.")

            return redirect("order_success", order_id=order.id)

    else:
        form = CheckoutForm(
            initial={
                "full_name": request.user.get_full_name(),
                "email": request.user.email,
            }
        )

    return render(
        request,
        "orders/checkout.html",
        {
            "form": form,
            "items": items,
            "total": total,
        },
    )


@login_required
def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    return render(
        request,
        "orders/order_success.html",
        {
            "order": order,
        },
    )


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/my_orders.html", {"orders": orders})

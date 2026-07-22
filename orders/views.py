from django.shortcuts import render

from decimal import Decimal

from django.shortcuts import get_object_or_404, redirect, render

from cart.views import cart_detail
from products.models import Product

from .forms import CheckoutForm
from .models import Order, OrderItem


def checkout(request):

    cart = request.session.get("cart", {})

    if not cart:
        return redirect("cart")

    items = []
    total = Decimal("0.00")

    for product_id, quantity in cart.items():

        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity

        total += subtotal

        items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    if request.method == "POST":

        form = CheckoutForm(request.POST)

        if form.is_valid():

            order = form.save(commit=False)

            order.total = total

            order.save()

            for item in items:

                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    price=item["product"].price,
                )

            request.session["cart"] = {}

            return render(
                request,
                "orders/order_success.html",
                {"order": order},
            )

    else:
        form = CheckoutForm()

    return render(
        request,
        "orders/checkout.html",
        {
            "form": form,
            "items": items,
            "total": total,
        },
    )
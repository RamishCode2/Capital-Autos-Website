def cart_item_count(request):
    """Expose the total number of units in the session cart to every template."""
    cart = request.session.get("cart", {})
    if not isinstance(cart, dict):
        return {"cart_item_count": 0}
    quantities = []
    for quantity in cart.values():
        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            continue
        if quantity > 0:
            quantities.append(quantity)
    return {"cart_item_count": sum(quantities)}

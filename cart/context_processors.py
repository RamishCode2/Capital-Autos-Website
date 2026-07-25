def cart_item_count(request):
    """Expose the total number of units in the session cart to every template."""
    cart = request.session.get("cart", {})
    return {"cart_item_count": sum(cart.values())}

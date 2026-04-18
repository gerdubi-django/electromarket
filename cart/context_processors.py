def cart_items_count(request):
    if request.user.is_authenticated and hasattr(request.user, "cart"):
        return {"cart_items_count": request.user.cart.items.count()}
    return {"cart_items_count": 0}

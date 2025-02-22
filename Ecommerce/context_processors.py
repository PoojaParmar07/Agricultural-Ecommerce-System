from .models import Cart

def cart_count(request):
    """Returns the total count of items in the user's cart"""
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        count = cart.total_cart_items() if cart else 0
    else:
        count = 0
    return {'cart_count': count}

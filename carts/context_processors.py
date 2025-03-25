from .models import Cart

def cart_count(request):
    """
    Context processor to add cart item count to all templates.
    """
    count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.items.count()
        except Cart.DoesNotExist:
            pass
    
    return {'cart_count': count} 
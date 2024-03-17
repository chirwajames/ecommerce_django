from .cart import Cart

# Create content processor can work on all pages of site


def cart(request):
    return {'cart': Cart(request)}
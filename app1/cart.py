from app1.models import Ecommerce_Product


class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get The current session key, Returning user
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages

        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        print(product_id)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = (product_qty)
        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        product_ids = self.cart.keys()
        products = Ecommerce_Product.objects.filter(id__in=product_ids)

        return products
    def cart_total(self,):
        product_ids = self.cart.keys()

        products = Ecommerce_Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0

        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + product.sale_price
                    else:
                        total = total + product.price

        return total

    def delete(self,product):
        product_id = str(product)
        # Delete from dictionary
        print('Key', product_id)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

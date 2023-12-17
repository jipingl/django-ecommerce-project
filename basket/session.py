from _decimal import Decimal

from store.models import Product


class Basket:
    def __init__(self, request):
        """
        Initialize the basket
        """
        if 'basket' not in request.session:
            request.session['basket'] = {}
        self.basket = request.session['basket']
        self.session = request.session

    def add(self, product, qty):
        """
        Add and update the users basket session data
        """
        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = int(qty)
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': int(qty)}
        self.save()

    def delete(self, product_id):
        """
        Delete item from session data
        """
        product_id = str(product_id)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def update(self, product_id, qty):
        """
        Update values in session data
        """
        product_id = str(product_id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
            self.save()

    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item['qty'] for item in self.basket.values())

    def __iter__(self):
        """
        Collect the product_id in the session data to query the database and return products
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()
        for product in products:
            basket[str(product.id)]['product'] = product
        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def save(self):
        """
        Save the basket session
        """
        self.session.modified = True

    def clear(self):
        del self.session['basket']
        self.save()

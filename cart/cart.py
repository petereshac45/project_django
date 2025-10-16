from decimal import Decimal
from products.models import Product

CART_SESSION_ID = "cart"

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        self.session[CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product_id, qty=1):
        product_id = str(product_id)
        item = self.cart.get(product_id)
        if item:
            item["qty"] += qty
        else:
            self.cart[product_id] = {"qty": qty}
        self.save()

    def set(self, product_id, qty):
        product_id = str(product_id)
        if qty <= 0:
            self.remove(product_id)
        else:
            self.cart[product_id] = {"qty": qty}
            self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session.pop(CART_SESSION_ID, None)
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids, is_available=True)
        pmap = {str(p.id): p for p in products}
        for pid, item in list(self.cart.items()):
            product = pmap.get(pid)
            if not product:
                self.remove(pid)
                continue
            qty = int(item["qty"])
            unit_price = Decimal(product.price)
            yield {
                "product": product,
                "qty": qty,
                "unit_price": unit_price,
                "line_total": unit_price * qty,
            }

    def totals(self):
        subtotal = sum(i["line_total"] for i in self)
        return {"subtotal": subtotal, "grand_total": subtotal}

    def count(self):
        return sum(int(i["qty"]) for i in self.cart.values())

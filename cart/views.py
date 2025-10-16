from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from products.models import Product
from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    context = {"cart_items": list(cart), "totals": cart.totals()}
    return render(request, "cart/cart_detail.html", context)

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id, is_available=True)
    qty = int(request.POST.get("qty", 1))

    if qty < 1:
        messages.warning(request, "الكمية لا بد أن تكون 1 على الأقل.")
        return redirect(request.META.get("HTTP_REFERER", "product_list"))

    if qty > product.stock:
        messages.error(request, "الكمية المطلوبة أكبر من المتاح حالياً.")
        return redirect(request.META.get("HTTP_REFERER", "product_list"))

    existing = cart.cart.get(str(product.id), {}).get("qty", 0)
    if existing + qty > product.stock:
        messages.error(request, "الكمية الإجمالية تتجاوز المخزون.")
        return redirect(request.META.get("HTTP_REFERER", "product_list"))

    cart.add(product.id, qty)
    messages.success(request, f"تم إضافة {product.name} إلى السلة.")
    return redirect(request.META.get("HTTP_REFERER", "product_list"))

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    new_qty = int(request.POST.get("qty", 1))

    if new_qty < 0:
        messages.warning(request, "قيمة كمية غير صالحة.")
        return redirect("cart_detail")
    if new_qty == 0:
        cart.remove(product.id)
        messages.info(request, f"تم حذف {product.name}.")
        return redirect("cart_detail")
    if new_qty > product.stock:
        messages.error(request, "الكمية المطلوبة أكبر من المخزون.")
        return redirect("cart_detail")

    cart.set(product.id, new_qty)
    messages.success(request, "تم تحديث الكمية.")
    return redirect("cart_detail")

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    messages.info(request, "تم حذف العنصر من السلة.")
    return redirect("cart_detail")

@require_POST
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, "تم تفريغ السلة.")
    return redirect("cart_detail")

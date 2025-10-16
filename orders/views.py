from django.db.models import F, Case, When, Value, BooleanField
from decimal import Decimal
from django.db import transaction
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from cart.cart import Cart
from products.models import Product
from .models import Order, OrderItem
from .forms import CheckoutForm


def checkout_view(request):
    cart = Cart(request)
    items = list(cart)
    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("cart_detail")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                product_ids = [it["product"].id for it in items]
                products = Product.objects.select_for_update().filter(pk__in=product_ids)
                pmap = {p.id: p for p in products}

                for it in items:
                    p = pmap[it["product"].id]
                    if it["qty"] > p.stock:
                        messages.error(request, f"The requested quantity of {p.name} is not available.")
                        return redirect("cart_detail")

                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    full_name=form.cleaned_data["full_name"],
                    phone=form.cleaned_data["phone"],
                    address=form.cleaned_data["address"],
                    status="pending",
                    total_amount=Decimal("0.00"),
                )

                total = Decimal("0.00")
                for it in items:
                    p = pmap[it["product"].id]
                    qty = it["qty"]
                    unit_price = Decimal(p.price)
                    line_total = unit_price * qty

                    OrderItem.objects.create(
                        order=order,
                        product=p,
                        quantity=qty,
                        unit_price=unit_price,
                        line_total=line_total,
                    )

                    rows = Product.objects.filter(pk=p.id, stock__gte=qty).update(
                        stock=F("stock") - qty,
                        is_available=Case(
                            When(stock__lte=qty, then=Value(False)),
                            default=F("is_available"),
                            output_field=BooleanField(),
                        ),
                    )

                    if rows == 0:
                        messages.error(request, f"The requested quantity of {p.name} is no longer available.")
                        return redirect("cart_detail")

                    total += line_total

                order.total_amount = total
                order.save(update_fields=["total_amount"])

                cart.clear()
                return redirect("checkout_success", order_id=order.id)
    else:
        form = CheckoutForm()

    subtotal = sum(Decimal(i["line_total"]) for i in items)
    context = {
        "form": form,
        "cart_items": items,
        "totals": {"subtotal": subtotal, "grand_total": subtotal},
    }
    return render(request, "orders/checkout.html", context)


def checkout_success(request, order_id):
    order = (
        Order.objects
        .prefetch_related("items__product")
        .get(pk=order_id)
    )
    return render(request, "orders/success.html", {"order": order})

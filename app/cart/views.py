from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form})

from django.shortcuts import redirect
from django.contrib import messages
from .cart import Cart  # Asegúrate de usar la clase que maneja tu carrito

def cart_update(request, product_id):
    cart = Cart(request)
    action = request.POST.get("action")
    quantity = request.POST.get("quantity")

    try:
        quantity = int(quantity)
        if action == "increase":  # Incrementa la cantidad
            cart.add(product_id, quantity=1, override_quantity=False)
        elif action == "decrease":  # Decrementa la cantidad
            cart.add(product_id, quantity=-1, override_quantity=False)
        else:  # Actualiza con el valor manual ingresado
            if quantity > 0:
                cart.add(product_id, quantity=quantity, override_quantity=True)
            else:
                messages.error(request, "La cantidad debe ser mayor a 0.")
    except ValueError:
        messages.error(request, "Cantidad inválida.")

    return redirect('cart:cart_detail')


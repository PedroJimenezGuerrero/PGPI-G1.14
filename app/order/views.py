from django.shortcuts import render, get_object_or_404
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])
            # clear the cart
            cart.clear()
            return render(request, 'order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'order/create.html', {'cart': cart, 'form': form})

def search(request):
    context = {}
    if request.method == "POST":
        order_code = request.POST.get("order_code")
        try:
            order = Order.objects.get(code=order_code)
            context['order'] = order
            context['items'] = order.items.all()
        except:          
            context['error'] = "No existe pedido con dicho localizador"

    return render(request, "order/search.html", context)

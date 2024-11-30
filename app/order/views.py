from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form_data = {
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'email': request.POST.get('email'),
                'address': request.POST.get('address'),
                'postal_code': request.POST.get('postal_code'),
                'city': request.POST.get('city'),
            }
            form = OrderCreateForm(form_data, user=request.user)
            if form.is_valid():
                # Crear la orden
                order = form.save()
                for item in cart:
                    price += item['quantity'] * item['price']
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )
                # Agregar datos de PayPal a la orden
                order.transaction_id = request.POST.get('transaction_id')
                order.status = request.POST.get('status')
                order.save()
                
                # Limpiar el carrito
                cart.clear()

                # Responder con datos de éxito
                #redirect_url = reverse('paypal_order_created', kwargs={'order_id': order.id})
                #return JsonResponse({'order_id': order.id, 'status': 'success'})
                return render(request, 'order/created.html', {'order': order})

            return JsonResponse({'error': 'Formulario inválido'}, status=400)
        else:
            form = OrderCreateForm(request.POST, user=request.user)
            if form.is_valid():
                order = form.save()
                for item in cart:
                    OrderItem.objects.create(order=order, product=item['product'],
                                            price=item['price'], quantity=item['quantity'])
                # clear the cart
                cart.clear()
                return render(request, 'order/created.html', {'order': order})
    else:
        form = OrderCreateForm(user=request.user)
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

from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib import messages
from .models import Order, OrderItem
from .forms import OrderCreateForm

from cart.cart import Cart
from django.conf import settings
from django.template.loader import render_to_string


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
                # send email
            name = form.cleaned_data['first_name']
            surname = form.cleaned_data['last_name']
            username_email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            postal_code = form.cleaned_data['postal_code']
            city = form.cleaned_data['city']
            code = order.code
            subject = 'Gracias por tu pedido!'

            total_cost = order.get_total_cost()
            if order.payment_method == 'contrareembolso':
                total_cost += 5

            email = EmailMessage(
                subject,
                f'Gracias por tu pedido, {name} {surname}.\n\n'
                f'Hemos recibido tu pedido con el código {code}.\n\n'
                f'Con un importe de {total_cost}€.\n\n'
                f'Dirección de envío:\n{address}, {postal_code} {city}\n'
                'Si tienes alguna duda, por favor, contacta con nosotros en AcademiaTerminus@cleon.com',
                to=[username_email]
            )
            email.fail_silently = False
            email.send()
            messages.success(request, 'Pedido realizado con éxito')
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
            total_price = order.get_total_cost()
            if order.payment_method == 'contrareembolso':
                total_price += 5
            context['order'] = order
            context['items'] = order.items.all()
            context['total_price'] = total_price
        except Order.DoesNotExist:          
            context['error'] = "No existe pedido con dicho localizador"

    return render(request, "order/search.html", context)

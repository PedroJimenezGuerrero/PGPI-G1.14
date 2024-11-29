from django.shortcuts import render
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

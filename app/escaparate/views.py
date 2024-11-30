from django.shortcuts import render, redirect, get_object_or_404
from cart.forms import CartAddProductForm
from shop.models import Category, Duration, Product
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from shop.models import Product
from cart.cart import Cart
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator

# from django.views import generic

# class IndexView(generic.ListView):
#     template_name = 'shop/index.html'
#     context_object_name = 'products'

#     def get_queryset(self):
#         '''Return five lattest products
#         '''
#         return Product.objects.filter(created__lte=timezone.now()
#         ).order_by('-created')[:5]

def escaparate(request):
    # Obtener los 2 productos más baratos
    cheapest_products = Product.objects.all().order_by('price')[:2]
    
    # Obtener el producto más caro
    most_expensive_product = Product.objects.all().order_by('-price').first()
    
    # Combinar los productos en una lista
    products_to_display = list(cheapest_products)
    if most_expensive_product:
        products_to_display.append(most_expensive_product)
    
    context = {
        'products': products_to_display,
    }
    return render(request, 'escaparate/escaparate.html', context)
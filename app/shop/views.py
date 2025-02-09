from django.shortcuts import render, redirect, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Duration, Product
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from shop.models import Product
from cart.cart import Cart
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator
from .models import Product
from django.db.models import Avg
from django.db.models import Q



def product_list(request):
    category_slugs = request.GET.getlist('category')
    duration_slugs = request.GET.getlist('duration')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    query = request.GET.get('q')

    query = request.GET.get('q')


    products = Product.objects.all()

    if category_slugs:
        products = products.filter(category__slug__in=category_slugs)

    if duration_slugs:
        products = products.filter(duration__slug__in=duration_slugs)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if query:
        products = products.filter(Q(name__icontains=query) | Q(category__name__icontains=query))

    paginator = Paginator(products, 6)  # Muestra 6 productos por página
    page = request.GET.get('page')
    products = paginator.get_page(page)
    

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'durations': Duration.objects.all(),
    }
    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    cart_product_form = CartAddProductForm()
    context = {'product': product, 'cart_product_form': cart_product_form}
    return render(request, 'shop/product/detail.html', context)


def terminos(request):
    return render(request, 'shop/terminos/terminos.html')

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

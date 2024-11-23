from django.shortcuts import render, redirect, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Duration, Product
from django.contrib.auth import logout

# from django.views import generic

# class IndexView(generic.ListView):
#     template_name = 'shop/index.html'
#     context_object_name = 'products'

#     def get_queryset(self):
#         '''Return five lattest products
#         '''
#         return Product.objects.filter(created__lte=timezone.now()
#         ).order_by('-created')[:5]



def product_list(request):
    category_slugs = request.GET.getlist('category')
    duration_slugs = request.GET.getlist('duration')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.filter(available=True)

    if category_slugs:
        products = products.filter(category__slug__in=category_slugs)

    if duration_slugs:
        products = products.filter(duration__slug__in=duration_slugs)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'durations': Duration.objects.all(),
    }
    return render(request, 'shop/product/list.html', context)

# class ProductListView(generic.ListView):
#     template_name = 'shop/product/list.html'

#     def get_queryset(self):
#         return Product.objects.filter(available=True)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         category = None
#         if category_slug:
#             category = get_object_or_404(Category, slug=category_slug)
#         context['category'] = category
#         context['categories'] = Category.objects.all()





def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    context = {'product': product, 'cart_product_form': cart_product_form}
    return render(request, 'shop/product/detail.html', context)


# class ProductDetialView(generic.DetailView):

#     template_name = 'shop/product/detail.html'
#     model = Product
#     form_class = CartAddProductForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['products'] = get_object_or_404(Product, 
#         id=id, slug=slug, available=True)
#         return context

def terminos(request):
    return render(request, 'shop/terminos/terminos.html')
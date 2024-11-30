"""config URL Configuration"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('order/', include('order.urls', namespace='order')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('accounts/', include('accounts.urls', namespace= 'accounts')),
    path('shop/', include('shop.urls', namespace='shop')), 
    path('', include('escaparate.urls', namespace='escaparate')), 
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# admin.site.site_header = "Mondongo :)"
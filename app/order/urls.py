from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('search', view=views.search, name='search'),
    path('modify/', view=views.order_modification, name='order_modification'),
    path('order/created/<int:order_id>/', views.order_create, name='paypal_order_created'),
]
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('duration/<slug:duration_slug>/', views.product_list, name='product_list_by_duration'),
    path('category/<slug:category_slug>/duration/<slug:duration_slug>/', views.product_list, name='product_list_by_category_duration'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
from django.urls import path
from . import views

app_name = 'administrador'

urlpatterns = [
    path('', views.vista_administrador, name='administrador'),
]

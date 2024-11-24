# from django.test import TestCase, Client
# from django.utils import timezone
# from cart.cart import Cart
# from shop.models import Category, Product
# from django.urls import reverse, resolve

# class CartTest(TestCase):
#     def setUp(self):
#         self.category = Category.objects.create(name='fastfood', slug='fastfood',)
#         self.product1 = Product.objects.create(category=self.category,
#                                               name='product1',
#                                               price=10,
#                                               created=timezone.now(),
#                                               updated=timezone.now())      
#         self.product2 = self.product = Product.objects.create(category=self.category,
#                                               name='product2',
#                                               price=100,
#                                               created=timezone.now(),
#                                               updated=timezone.now())   
#         self.url1 = reverse('cart:cart_add', args=[self.product1.id]) 
#         self.url2 = reverse('cart:cart_add', args=[self.product1.id]) 
#         self.client = Client()
    
#     def test_add_test(self):
#         response = self.client.post(self.url1, data={'first_name' :'user',
#                                                      'last_name':1,
#                                                      'email': 'user1@org.com',
#                                                      'address': 'user1 st. 123',
#                                                      'postal_code': '0001',
#                                                      'city': 'userpolis',
#                                                     })
#         self.assertEqual(response.status_code, 302)
from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, Category
from django.utils import timezone
from django.contrib.auth.models import User

class CartTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='fastfood', slug='fastfood',)
        self.product = Product.objects.create(category=self.category,
                                              name='product1',
                                              price=10,
                                              created=timezone.now(),
                                              updated=timezone.now()) 
        # self.client.login(username='testuser', password='testpassword')

    def test_cart_detail_view(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')

    def test_cart_add_view(self):
        response = self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 1, 'update': False})
        self.assertEqual(response.status_code, 302)  # Redirige después de añadir al carrito
        self.assertRedirects(response, reverse('cart:cart_detail'))

    def test_cart_remove_view(self):
        # Primero, añadir un producto al carrito
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 1, 'update': False})
        # Ahora, eliminar el producto del carrito
        response = self.client.post(reverse('cart:cart_remove', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirige después de eliminar del carrito
        self.assertRedirects(response, reverse('cart:cart_detail'))

    def test_cart_add_invalid_product(self):
        invalid_product_id = 999  # ID de producto que no existe
        response = self.client.post(reverse('cart:cart_add', args=[invalid_product_id]), {'quantity': 1, 'update': False})
        self.assertEqual(response.status_code, 404)  # Debería devolver un 404 ya que el producto no existe

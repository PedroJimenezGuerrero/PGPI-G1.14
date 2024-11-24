from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Category, Product
from cart.cart import Cart


class TestViews(TestCase):

    def test_order_create_view(self):
        response = self.client.get(reverse('order:order_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/create.html')

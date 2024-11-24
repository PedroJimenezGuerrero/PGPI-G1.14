from order.views import *
from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestUrls(SimpleTestCase):

    def test_create_url(self):
        url = reverse('order:order_create')
        self.assertEqual(resolve(url).func, order_create)

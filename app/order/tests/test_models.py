from django.test import TestCase
from django.utils import timezone
from order.models import Order, OrderItem
from shop.models import Product, Category

class OrderTest(TestCase):
    
    def setUp(self):
        self.order1 = Order.objects.create(first_name="joselito",
                                 last_name='el gallo',
                                 email='eljose@email.com',
                                 address = 'C/ Joselito el gallo S/N',
                                 city = 'Dose Hermanas',
                                 postal_code= '41714',)
        
    def test_order_creation(self):
        self.assertTrue(isinstance(self.order1, Order))
        self.assertEqual(self.order1.__str__(), 'Order {}'.format(self.order1.id))
        self.assertEqual(self.order1.get_total_cost(), 0)
        
    def test_order_cost(self):
        self.category = Category.objects.create(name='fastfood', slug='fastfood',)
        self.product = Product.objects.create(category=self.category,
                                              name='product',
                                              price=10,
                                              created=timezone.now(),
                                              updated=timezone.now())
        self.i1 = OrderItem.objects.create(order = self.order1,
                                           product=self.product,
                                           price = 10,
                                           quantity = 2)
        
        self.assertEqual(self.order1.get_total_cost(), 20)
        

class OrderItemTest(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(name='fastfood', slug='fastfood',)
        self.product = Product.objects.create(category=self.category,
                                              name='product',
                                              price=10,
                                              created=timezone.now(),
                                              updated=timezone.now())
        self.order1 = Order.objects.create(first_name="joselito",
                                 last_name='el gallo',
                                 email='eljose@email.com',
                                 address = 'C/ Joselito el gallo S/N',
                                 city = 'Dose Hermanas',
                                 postal_code= '41714',)
    

    def test_OrderItem_creation(self):
        self.i1 = OrderItem.objects.create(order = self.order1,
                                           product=self.product,
                                           price = 10,
                                           quantity = 2)
        self.assertTrue(isinstance(self.i1, OrderItem))
        self.assertEqual(self.i1.__str__(), '{}'.format(self.i1.pk))
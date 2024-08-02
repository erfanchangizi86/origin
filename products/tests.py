from django.test import TestCase

from products.models import Product, Comment_product


# Create your tests here.


class ProductTests(TestCase):
    def setUp(self):
        Comment_product.objects.create(title='erfan')

    def test_product_is_active(self):
        product=Comment_product.objects.get(title='erfan')
        self.assertEqual(product.title,'erfan')
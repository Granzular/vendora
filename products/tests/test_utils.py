from django.test import TestCase
from ..models import Category,Product
from ..utils import *

class TestGetProductsByCategory(TestCase):

    def setUp(self):
        cat = Category.objects.create(name="test_cat")
        product = Product.objects.create(name="book",description="book black",price=600)
        product.category.add(cat)


    def test_with_existing_category(self):
        self.assertIsNotNone(get_products_by_category("test_cat"))

    def test_with_nonexisting_category(self):
        with self.assertRaises(Category.DoesNotExist):
            get_products_by_category("no_cat")


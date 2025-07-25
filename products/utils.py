"""Contains utility and services for interacting with the products app"""
from .models import Product,Category

def get_products_by_category(category):
    """ Returns a queryset of product related to the given category. it raises a Category.DoesNotExist if the given category does not exist"""

    category = Category.objects.get(name=category)
    product_list = Product.objects.filter(category=category)

    return product_list

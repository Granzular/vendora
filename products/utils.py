"""Contains utility and services for interacting with the products app"""
from .models import Product,Category,Review,Inventory

def get_products_by_category(category_name):
    """ Returns a queryset of product related to the given category. it raises a Category.DoesNotExist if the given category does not exist"""

    category = Category.objects.get(name=category_name)
    product_list = Product.objects.filter(category=category)

    return product_list

def get_product_reviews(product):

    reviews = Review.objects.filter(product=product)

    return reviews



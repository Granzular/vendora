"""Contains utility and services for interacting with the products app"""
from .models import Product,Category,Review,Inventory

def get_products_by_category(category_name):
    """ Returns a queryset of product related to the given category. it returns None if the category does not exit, and [] if no product exists in the category"""

    if category_name.lower() == "all":
        category = Category.objects.all()
    else:
        category = Category.objects.filter(name=category_name.lower())
    if category:
        category = category[0]
    else:
        return None

    product_list = Product.objects.filter(category=category)

    return product_list

def get_product_reviews(product):

    reviews = Review.objects.filter(product=product)

    return reviews

def get_product_by_id(pk):
    return Product.objects.get(id=pk)

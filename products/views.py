from django.shortcuts import render 
from .models import Product,Category
from django.views.generic import ListView
from .utils import get_product_reviews, get_products_by_category

def detailView(request,pk):
    product = Product.objects.get(id=pk)
    reviews = get_product_reviews(product)
    
    context = {
            "product" : product,
            "product_reviews" : reviews,
            }
    return render(request,"products/detail.html",context)

class CategoryListView(ListView):
    model = Category
    template_name = "products/category_list.html"
    object_name = "category_list"

def category_products_view(request,category_name):
    
    products = get_products_by_category(category_name)
    context = {
            "products":products,
            "category":category_name,
            }
    """This view renders a template that uses a template partial, so the key "products" and any other key must be cobsistent"""
    return render(request,"products/category_products.html",context)

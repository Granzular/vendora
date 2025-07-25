from django.shortcuts import render
from products.utils import get_products_by_category

def index(request):

    products = get_products_by_category("featured")
    context = {
            "products":products
            }
    return render(request,'store/index.html',context)



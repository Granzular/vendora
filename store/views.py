from django.shortcuts import render
from products.utils import get_products_by_category
from orders.utils import get_cart_by_user
def index(request):

    featured = get_products_by_category("featured")
    products = get_products_by_category("all")
    try:
        cart = get_cart_by_user(request.user)["response"]
    except:
        cart = None
    context = {
            "featured":featured,
            "products":products,
            "cart":cart,
            }
    return render(request,'store/index.html',context)

def hero(request):
    return render(request,'store/hero.html')

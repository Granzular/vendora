from django.shortcuts import render
from .models import Cart

def orders_list_view(request,status):
    
    if status == "all":
        orders = Cart.objects.all()
    else:
        orders = Cart.objects.filter(status=status)

    context = {
            "orders":orders
            }
    return render(request,"orders/orders_list.html",context)


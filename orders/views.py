from django.shortcuts import render
from .models import Order
from .utils import get_orders_list_by_user,get_order_by_user
from django.contrib.auth.decorators import login_required

@login_required
def orders_list_view(request,status):

    orders_list = get_orders_list_by_user(status,request.user)
    if orders_list.get("error"):
        orders_list = None
    elif orders_list.get("response"):
        orders_list = orders_list.get("response")

    context = {
            "orders":orders_list
            }
    return render(request,"orders/list.html",context)

@login_required
def orders_detail_view(request,pk):

    order = get_order_by_user(pk,request.user)
    context = {
            "order": order
            }

    return render(request,"orders/detail.html",context)

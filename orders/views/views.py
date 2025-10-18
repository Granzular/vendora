from django.shortcuts import render
from ..models import Order
from ..utils import get_orders_list_by_user,get_order_by_user, get_cart_by_user, add_to_cart, remove_from_cart
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json
from django.core import serializers

@login_required
def orders_list_view(request,status):

    orders_list = get_orders_list_by_user(status,request.user)
    if orders_list.get("error"):
        orders = None
    elif orders_list.get("response"):
        orders = orders_list.get("response")
    else:
        orders = None

    context = {
            "orders":orders
            }
    return render(request,"orders/list.html",context)

@login_required
def orders_detail_view(request,pk):

    order = get_order_by_user(pk,request.user)
    context = {
            "order": order
            }

    return render(request,"orders/detail.html",context)

@login_required
def cart_view(request):
    if request.method == "GET":
        if request.headers.get("X-Requested-With")=="XMLHttpRequest":
            cart = get_cart_by_user(request.user)["response"]
            context = {
                    "totalCartPrice" : cart.total_price(),
                    "cartCount" : len(cart.positions.all()),
                    "cartItems" :[],
                    "cart" : []
                    }
            for item in  cart.positions.all():
                context["cartItems"].append({"price":item.product.price,"subTotal":item.total_price(),"product":item.product.id,"quantity":item.quantity})
            for item in cart.positions.all():
                context["cart"].append({"product":item.product.id,"quantity":item.quantity})
            return JsonResponse(context)
        else:
            cart = get_cart_by_user(request.user)["response"]
            empty = True if len(cart.positions.all())<=0 else False

            context = {
                    "cart" : cart,
                    "empty": empty,
                    }
            return render(request,"orders/cart_view.html",context)

    elif request.method == "POST":
        if request.headers.get("X-Requested-With")=="XMLHttpRequest":
            data = json.loads(request.body)
            res = add_to_cart(request.user,data)
            return JsonResponse({"res":res},status=200)
    elif request.method == "DELETE":
        if request.headers.get("X-Requested-With")=="XMLHttpRequest":
            data = json.loads(request.body)
            remove_from_cart(request.user,data["product"])
            return JsonResponse({},status=200)
    elif request.method == "UPDATE":
        if request.headers.get("X-Requested-With")=="XMLHttpRequest":
            data = json.loads(request.body)
            res = remove_from_cart(request.user,data["product"],update=True)
            return JsonResponse({"res":res},status=200)



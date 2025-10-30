from django.shortcuts import render
from ..models import Order
from ..utils import get_orders_list_by_user,get_order_by_user, get_cart_by_user, add_to_cart, remove_from_cart, create_order
from ..forms import CheckoutForm
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
    elif request.method == "PATCH":
        if request.headers.get("X-Requested-With")=="XMLHttpRequest":
            data = json.loads(request.body)
            res = remove_from_cart(request.user,data["product"],update=True)
            return JsonResponse({"res":res},status=200)

@login_required
def checkout(request):
    
    if request.method == "GET":

        cart = get_cart_by_user(request.user)["response"]
        fname = request.user.first_name
        lname = request.user.last_name
        email = request.user.email
        cust = request.user.customer_set.all()[0]
        addr = cust.address
        phone = cust.phone

        checkout_form = CheckoutForm(initial={"first_name":fname,"last_name":lname,"email":email,"delivery_address":addr,"phone":phone})
        context = {
                "checkout_form" : checkout_form,
                "cart" : cart

                }
        return render(request,"orders/checkout.html",context)

    elif request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data.get("first_name")
            lname = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            addr  = form.cleaned_data.get("delivery_address")
            phone = form.cleaned_data.get("phone")
            # create order
            order = create_order(request.user)

            # initialize payment

            return HttpResponse("<h1>Ok</h1>")
        else:
            return HttpResponse("<h1>NOT OK</h1>",status=400)

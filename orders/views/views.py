from django.shortcuts import render, reverse, redirect
from ..models import Order
from ..utils import get_orders_list_by_user,get_order_by_user, get_cart_by_user, add_to_cart, remove_from_cart, create_order
from ..forms import CheckoutForm
from payments.paystack import PaystackClient
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json
from django.core import serializers
from django.conf import settings

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
            cart = get_cart_by_user(request.user)
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

        cart = get_cart_by_user(request.user)
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
            amount = order.total_price

            # initialize payment
            paycl = PaystackClient()
            callback_url =  settings.HOST_BASE_URL + (reverse("orders:verify_payment"))
            res = paycl.initialize_payment(email,amount,callback_url=callback_url)
            if res.get("status") == True:
                data = res["data"]
                auth_url = data["authorization_url"]
                reference = data["reference"]
                order.payment_reference = reference
                order.save()
                print(auth_url)
                return redirect(auth_url)
            else:
                return HttpResponse("<h1> An Error Occurred. Try again or Conatct Support"+str(res),status=500)

        else:
            return HttpResponse("<h1>NOT OK</h1>",status=400)

def verify_payment(request):
    if request.method == "GET":
        reference = request.GET.get("reference")
        order = Order.objects.filter(payment_reference= reference)
        order = order[0] if len(order)>0 else None

        if order:
            paycl = PaystackClient()
            res = paycl.verify_payment(reference)
            rstatus = res.get("data").get("status")
            status = paycl.get_status(rstatus)
            amount = res.get("data").get("amount") / 100
            if status == "success" and amount == order.total_price:
                order.payment_status = "processing"
                order.save()
                return HttpResponse("<h1>Order Processing</h1>")
            else:
                return HttpResponse(f"<h1>Unknown Response{rstatus}",status=400)

        else:
            return HttpResponse("<h1>Reference Mismatch. Contact support</h1>")

def paystack_webhook(request):
    if request.method == "POST":
        pass

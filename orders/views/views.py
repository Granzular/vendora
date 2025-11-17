from django.shortcuts import render, reverse, redirect
from ..models import Order, Transaction
from ..utils import get_orders_list_by_user,get_order_by_user, get_cart_by_user, add_to_cart, remove_from_cart, create_order, create_transaction
from ..forms import CheckoutForm
from payments.paystack import PaystackClient
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json, hmac, hashlib, logging
from django.core import serializers
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

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
                # create transaction
                trans = create_transaction(order,reference)
                return redirect(auth_url)
            else:
                return HttpResponse("<h1> An Error Occurred. Try again or Conatct Support"+str(res),status=500)

        else:
            return HttpResponse("<h1>NOT OK</h1>",status=400)

@login_required
def retry_payment(request):
    pass

@login_required
def verify_payment(request):
    if request.method == "GET":
        reference = request.GET.get("reference")
        trans = Transaction.objects.filter(reference=reference)
        trans = trans[0] if len(trans)>0 else None
        order = trans.order

        if trans and order:
            paycl = PaystackClient()
            res = paycl.verify_payment(reference)
            rstatus = res.get("data").get("status")
            status = paycl.get_status(rstatus)
            amount = res.get("data").get("amount") / 100
            if status == "success" and amount == order.total_price:
                order.payment_status = "processing"
                order.save()
                context = {"message":"Your payment is being processed."}
                return render(request,"orders/payment_response.html",context)
            elif status == "failed" and amount == order.total_price:
                context = {"message":"Payment Declined. You can Retry"}
                return render(request,"orders/payment_response.html")
            else:
                return HttpResponse(f"<h1>Unknown Response{rstatus}",status=400)

        else:
            return HttpResponse("<h1>Reference Mismatch. Contact support</h1>")

@csrf_exempt
def paystack_webhook(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    raw_body = request.body
    try:
        payload = json.loads(raw_body)
        reference = payload.get("data",{}).get("reference")
        if reference:
            order_exists = Order.objects.filter(payment_reference = reference, status="paid").exists()
            if order_exists:
                #log
                return HttpResponse(status=200)
    except json.JSONDecodeError:
        # log error
        return HttpResponse(status=400)

    secret_key = settings.PAYSTACK_SECRET_KEY.encode()
    header_signature = request.headers.get("x-paystack-signature")
    computed_signature = hmac.new(secret_key,raw_body,hashlib.sha512).hexdigest()

    if not hmac.compare_digest(computed_signature,header_signature or ""):
        # log failure
        return HttpResponse(status=400)

    event_type = payload.get("event")
    data = payload.get("data",{})

    try:
        trans = Transaction.objects.get(reference=reference)
        if event_type == "charge.success" and reference:
            if trans.status != "success":
                trans.status = "success"
                trans.info = "transaction successful"
                trans.order.payment_reference = reference
                trans.order.status="paid"
                trans.order.paid_at = timezone.now()
                trans.order.save()
                trans.save()
                # log behaviour, check if webhook is redundant or efficiently indempotent.
        elif event_type == "charge.failed" and reference:
            if trans.status != "failed":
                trans.status = "failed"
                trans.info = "transaction failed"
                trans.save()
    except:
        # log error
        return HttpResponse(status=200)

    return HttpResponse(status=200)


        

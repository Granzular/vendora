from .models import Order, OrderPosition, Cart, CartPosition
from customers.models import Customer
from products.utils import get_product_by_id
from django.db.utils import IntegrityError
from django.http import Http404
def get_orders_list_by_user(status,user):
    """
    returns a dict that contains a the cart object that can be accessed with 'response' key. check for 'error' key for errors
    """
    
    try:
        customer = Customer.objects.get(user=user)
        if status == "all":
            order = Order.objects.filter(customer=customer)
        else:
            order = Order.objects.filter(customer=customer,status=status)
        if len(order) == 0:
            order = None
        

        return {"response":order}
    
    except Customer.DoesNotExist as err:
        return {"error":err}

def get_order_by_user(pk,user):

    try:
        customer = Customer.objects.get(user=user)
        order = Order.objects.get(customer=customer,id=pk)
        return order

    except Order.DoesNotExist as err:
        return None
def get_cart_by_user(user):
    
    try:
        customer = Customer.objects.get(user=user)
        cart = Cart.objects.get(customer=customer,status="active")
        return cart
    
    except Customer.DoesNotExist as err:
        raise Http404

    except Cart.DoesNotExist:
        cart = Cart.objects.create(customer=customer,status="active")
        return cart

def add_to_cart(user,data):

    cart = get_cart_by_user(user)
    if cart == None:
        return None
    product = get_product_by_id(data["product"])
    quantity = data["quantity"]
    try:
        CartPosition.objects.create(cart=cart,product=product,quantity=quantity)
    except IntegrityError:
        cart_item = CartPosition.objects.get(cart=cart,product=product)
        cart_item.quantity += 1
        cart_item.save()

    return True

def remove_from_cart(user,pk,update=False):
    cart = get_cart_by_user(user)
    if cart == None:
        return None
    cart_item = CartPosition.objects.get(cart=cart,id=pk)
    if update:
        cart_item.quantity -= 1
        if cart_item.quantity == 0:
            cart_item.delete()
            
        else:
            cart_item.save()
    else:
        cart_item.delete()
    return cart_item.quantity or None

def create_order(user):
    order = Order.objects.create(customer=user.customer_set.all()[0])
    cart = get_cart_by_user(user)
    if cart == None:
        return False
    for item in cart.positions.all():
        op = OrderPosition.objects.create(product=item.product,quantity=item.quantity,price=item.total_price())
        order.positions.add(op)

    order.save()
    cart.status = "checked_out" # sets current cart to inactive, triggers creation of a new one
    cart.save()
    return order

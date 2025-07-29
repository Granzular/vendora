from .models import Order
from customers.models import Customer

def get_orders_list_by_user(status,user):
    """
    returns a dict that contains a the cart object that can be accessed with 'response' key. check for 'error' key fir errors
    """
    
    try:
        customer = Customer.objects.get(user=user)
        if status == "all":
            order = Order.objects.filter(customer=customer)
        else:
            order = Order.objects.filter(customer=customer,status=status)

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


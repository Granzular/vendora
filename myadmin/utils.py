from orders.models import Sales


def get_sales():
    sales = Sales.objects.all()
    data = [{"product":x.product,"quantity":x.quantity,"time":x.created} for x in sales]

    return data


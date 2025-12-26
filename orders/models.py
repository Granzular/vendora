from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from decimal import Decimal
import uuid

from products.models import Product
from customers.models import Customer


# -----------------------
# CART & CART POSITIONS
# -----------------------
class Cart(models.Model):

    STATUS_CHOICES = (
            ("active","active"),
            ("checked_out","checked_out"),
            )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)  # for guest carts
    status = models.CharField(choices = STATUS_CHOICES,max_length=20,default="active")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(position.total_price() for position in self.positions.all())
    def total_cart(self):
        return len(self.positions.all())

    def __str__(self):
        return f"Cart {self.id} for {self.customer or 'Guest'}"


class CartPosition(models.Model):
    cart = models.ForeignKey(Cart, related_name="positions", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    class Meta:
        constraints = [
                models.UniqueConstraint(
                    fields=["cart","product"],
                    name = "unique_product_per_cart")
                ]

# -----------------------
# ORDER & ORDER POSITIONS
# -----------------------
class OrderPosition(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Unit price × quantity at time of purchase",blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def save(self, *args, **kwargs):
        if not self.price:  # only set if not manually provided
            self.price = Decimal(self.product.price) * self.quantity
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Order Positions"


class Order(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'In Progress'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    order_id = models.CharField(max_length=32, unique=True, editable=False, default=uuid.uuid4)
    positions = models.ManyToManyField(OrderPosition, related_name="orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20,default="")
    delivery_address = models.CharField(max_length=100,default="")
    status = models.CharField(choices=STATUS_CHOICES, max_length=30, default='in_progress')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True,blank=True)
    payment_status = models.CharField(max_length=20, default="unpaid")  # could be 'unpaid', 'paid', 'failed'
    payment_reference = models.CharField(max_length=100, blank=True, null=True)  # for gateway reference
    """ payment_status vs status.
        payment_status tracks payment while status tracks progress of order, from checkout→ payment→ delivery
    """

    def __str__(self):
        return f"Order {self.order_id} | {self.customer.user.username} | {self.status}"

    def get_absolute_url(self):
        return reverse("orders:detail", kwargs={"pk": self.id})

    def get_formatted_created(self):
        return self.created.strftime("%I:%M %p, %d %b %Y")

    def get_formatted_total_price(self):
        return "{:,.2f}".format(self.total_price or 0)

    def save(self, *args, **kwargs):
        super().save(*args,**kwargs)
        # auto-compute total_price
        if not self.total_price:
            self.total_price = sum(pos.price for pos in self.positions.all())
        super().save(update_fields=["total_price"])

    class Meta:
        ordering = ['-created']

class Transaction(models.Model):
    STATUS_CHOICES = (
            ("success","successful"),
            ("failed","failed"),
            ("pending","pending"),
            )
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    reference = models.CharField(max_length=100,unique=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,null=True,blank=True)#failed,successful,pending
    info = models.CharField(max_length=50,default=" ")
    payment_gateway = models.CharField(max_length=30,null=True,blank=True)
    payment_method = models.CharField(max_length=30,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.user.username}{self.status}"

    class Meta:
        ordering = ["-created"]

class Sales(models.Model):
    """ The sales model represents the sale of a particular product and the quantity sold for a given order. it is structurally an order position of a successful order. why a seprate model then? For decoupling, clarity and clear business logic and semantics"""

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product =  models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    created = models.DateTimeField(auto_now_add=True)

 

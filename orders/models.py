from django.db import models
from products.models import Product
from customers.models import Customer


class Position(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField(help_text='in Naira, auto compute!',blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} {self.product.name}"

    def save(self,*args,**kwargs):
        self.price = self.product.price * self.quantity
        return super().save(*args,**kwargs)



class Cart(models.Model):
    STATUS_CHOICES = (
            ('in_progress','in_progress'),
            ('delivered','delivered'),
            ('cancelled','cancelled'),
            )
    positions = models.ManyToManyField(Position)
    total_price = models.IntegerField(blank=True,null=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    status = models.CharField(choices = STATUS_CHOICES,max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    """ They total_price auto calculate witg the help of a signal in orders.signals.py
    """

    def __str__(self):
        return f"Cart {self.customer.user.username}|{self.status}"

from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from customers.models import Customer
from django.shortcuts import reverse

# Create your models here.

class Product(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ManyToManyField("Category")
    price = models.IntegerField(help_text='in Naira')
    image = models.ImageField(upload_to='products',null=True,blank=True)
    discount = models.IntegerField(validators=[MinValueValidator(1,message='min value is 1%'),MaxValueValidator(100,message='max value is 100%')],help_text='in percent',null=True,blank=True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.name

    def get_discount_price(self):
        if discount:
            return  self.price - (self.price * (discount/100))
    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"pk":self.id})

    def get_rating(self):
        reviews = self.review_set.all()
        if len(reviews)==0:
            return None
        else:
            rating = sum([x.rating for x in reviews])/len(reviews)
            return rating

    def get_quantity_in_inventory(self):
        try:
            quantity = None if self.inventory.quantity==0 else self.inventory.quantity
        except:
            return None

        return quantity


    class Meta:
        ordering = ['-created']

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True,null=True,blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:category_products",kwargs={"category_name":self.name})

    class Meta:
        verbose_name_plural = "Categories"



class Inventory(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name}=> {self.quantity}"

    class Meta:
        verbose_name_plural = "Inventories"


class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    text = models.TextField(default="")
    rating = models.IntegerField(validators=[MaxValueValidator(5)],default=5)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.user.username[:10]}=>{self.product.name}"


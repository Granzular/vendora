from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import  LoginRequiredMixin,UserPassesTestMixin
from django.utils.decorators import method_decorator
from products.models import Product, Category, Inventory
from customers.models import Customer
from django.http import JsonResponse
import random


class DashboardView(LoginRequiredMixin,UserPassesTestMixin , View):
    """ This view is the admin dashboard."""
    
    def test_func(self):
        # change is_supeeuser to groups
        return self.request.user.is_superuser

    def get(self,request):
        products = Product.objects.all()
        customers = Customer.objects.all()

        context = {
                "products" : products,
                "customers" : customers
                }
        return render(request,"myadmin/dashboard.html",context)

    def post(self,request):
        pass

def sales_view(request):

    data = [{"time": f"{hour:02d}:00", "value": random.randint(100, 400)}for hour in range(9, 24) ]

    return JsonResponse(data,safe=False)

def product_view(request):
    products = Product.objects.all()
    context = {
            "products" : products,
            }
    return render(request,"myadmin/products.html",context)

def inventory_view(request):
    inventory = Inventory.objects.all()
    context = {
            "inventory" : inventory,
            }
    return render(request,"myadmin/inventory.html",context)

def category_view(request):
    categories = Category.objects.all()
    context = {
            "categories" : categories,
            }
    return render(request,"myadmin/category.html",context)

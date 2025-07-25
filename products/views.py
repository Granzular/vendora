from django.shortcuts import render 
from .models import Product,Category
from django.views.generic import ListView

def detailView(request,pk):
    product = Product.objects.get(id=pk)
    context = {
            "product":product,
            }
    return render(request,"products/detail.html",context)

class CategoryListView(ListView):
    model = Category
    template_name = "products/category_list.html"
    object_name = "category_list"

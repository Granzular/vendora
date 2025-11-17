from django.contrib import admin
from .models import OrderPosition, Order,Cart, CartPosition, Transaction

admin.site.register(OrderPosition)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartPosition)
admin.site.register(Transaction)

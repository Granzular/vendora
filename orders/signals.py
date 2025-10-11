from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
import uuid
from .models import Order, OrderPosition
from products.models import Product




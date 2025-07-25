from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Cart

@receiver(m2m_changed,sender=Cart.positions.through)
def create_or_update_cart(sender,instance,action,**kwargs):
    
    instance.total_price = sum([item.price for item in instance.positions.all()])
    instance.save()
        

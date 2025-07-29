from django.db.models.signals import m2m_changed,post_save
from django.dispatch import receiver
from .models import Order
import uuid

@receiver(m2m_changed,sender=Order.positions.through)
def create_or_update_cart(sender,instance,action,**kwargs):
    
    instance.total_price = sum([item.price for item in instance.positions.all()])
    instance.save()
       
@receiver(post_save,sender=Order)
def create_order(sender,instance,created,**kwargs):

    if created:
        instance.order_id = str(uuid.uuid4())[:32]
        instance.save(update_fields=['order_id'])
        """ instance.save(update_fields=['order_id']) is used in favor of instance.save() in order to prevent recursive save; it also reduces overhead as it only saves the updated model, compared to the latter. This could also be achieved by overriding the model save() method; signals were used out of prefrence of decoupling and flexibility
        """

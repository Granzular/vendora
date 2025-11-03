"""
Context_processors for customers
"""
from .models import Notification

def notification(request):
    try:
        instance = Notification.objects.filter(user=request.user)
        new_instance = instance.filter(viewed=False)
        new_count = len(new_instance)
        total_count = len(instance)
        return {
            "new_notification" : new_instance,
            "notification" : instance,
            "new_count" : new_count,
            "total_count" : total_count,
            }
    except:
        return {}

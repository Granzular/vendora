"""
Context_processors for customers
"""
from .models import Notification

def notification(request):
    """ this context processor adds notification data to the context, enabling new notification to be displayed regardless of the view.
     NOTE: It would and should be replaced with webSockets instead. As this current implementation uses the philosophy of polling, which is grossly inefficient.
     """
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

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.shortcuts import reverse
import uuid
# Create your models here.

def send_notification(user,msg,url,category="general"):
    """ same function in customers.utils, added here to bypass circular importation issues """
    notification = Notification.objects.create(user=user,message=msg,category=category,url=url)
    return True


class CustomUser(AbstractUser):
    user_type = models.CharField(blank=True,null=True,max_length=30)
    """def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        send_notification(self,"Account Created",reverse("customers:profile"))"""

    def save(self,*args,**kwargs):

        if self.pk:
            old_instance = CustomUser.objects.get(pk=self.pk)
            if old_instance.username != self.username:
                send_notification(self,"Username Updated",reverse("customers:profile"))

            if old_instance.email != self.email:
                send_notification(self,"Email Updated",reverse("customers:profile"),category="security")

            if old_instance.first_name != self.first_name:
                send_notification(self,"First Name Updated",reverse("customers:profile"),category="security")
                
            if old_instance.last_name != self.last_name:
                send_notification(self,"Last Name Updated",reverse("customers:profile"),category="security")


            if old_instance.password != self.password:
                send_notification(self,"Password Updated",reverse("customers:profile"),category="security")

        super().save(*args,**kwargs)

             
class Customer(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    address = models.CharField(max_length=150,blank=True,null=True)
    phone = models.PositiveIntegerField(blank=True,null=True)
    avatar = models.ImageField(upload_to="profile",null=True,blank=True)

    
    def __str__(self):
        return self.user.username

    """def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        send_notification(self,"Profile Created. Take a look at your profile",reverse("customers:profile"))
"""
    def save(self,*args,**kwargs):
 
        if self.pk:
            old_instance = Customer.objects.get(pk=self.pk)
            if old_instance.address != self.address:
                send_notification(self.user,"Address Updated",reverse("customers:profile"))
            if old_instance.phone != self.phone:
                send_notification(self.user,"Phone Updated",reverse("customers:profile"),category="security")
            if old_instance.avatar.name != self.avatar.name:
                send_notification(self.user,"Profile picture Updated",reverse("customers:profile"),category="security")
        super().save(*args,**kwargs)

    def avatar_url(self):
        try:
            return self.avatar.url
        except ValueError:
            return '/media/images/icons/person.svg'

class EmailVerification(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    secret_key = models.CharField(blank=True,max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    @property
    def has_expired(self):
        return timezone.now() - self.created > timezone.timedelta(minutes=10)
    def save(self,*args,**kwargs):
        self.secret_key =  str(uuid.uuid4())
        super().save(*args,**kwargs)


class Notification(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    category = models.CharField(max_length=30,null=True,blank=True,default="general")
    viewed = models.BooleanField(default=False)
    url = models.CharField(max_length=150,default="/")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"self.user.username => self.message"
    
    def mark_as_viewed(self):
        self.viewed = True

    def get_css_class(self):
        if self.viewed:
            return ""
        else:
            return "new-notification"
    class Meta:
        ordering = ["-created"]

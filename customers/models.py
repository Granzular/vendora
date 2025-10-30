from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
# Create your models here.

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    address = models.CharField(max_length=150,blank=True,null=True)
    phone = models.PositiveIntegerField(blank=True,null=True)
    avatar = models.ImageField(upload_to="profile",null=True,blank=True)

    
    def __str__(self):
        return self.user.username

class EmailVerification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    secret_key = models.CharField(default="vendora-"+ str(uuid.uuid4()))
    created = models.DateTimeField(auto_now_add=True)
    @property
    def has_expired(self):
        return timezone.now() - self.created > timezone.timedelta(minutes=10)

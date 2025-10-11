from django.contrib.auth.signals import user_logged_in
from django.contrib import messages
from django.dispatch import receiver

@receiver(user_logged_in)
def greet_on_login(sender, request, user, **kwargs):
    messages.success(request, "login",extra_tags="login")

from django.shortcuts import reverse
from .models import EmailVerification as EV, Notification, CustomUser
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

def send_confirmation_email(email,username):
    user = CustomUser.objects.get(username=username)
    EV.objects.get_or_create(user = user )
    obj = EV.objects.get(user = user)

    if obj.has_expired:
        obj.delete()
        EV.objects.get_or_create(user = user)
        obj = EV.objects.get(user = user)
        print("new code created")
    url = "http://localhost:8000" + reverse('customers:verify_email',kwargs={'secret_key':obj.secret_key})
    print(url)
    print("Email: "+user.email)
    subject = "Email Verification"
    from_email = "ayenimichael92@gmail.com"
    to = [user.email]
    text_content = f"copy link to browser: {url}"
    html_content = f"<! DOCTYPE><html><head><meta charset='UTF-8'></head><body><p>Click the link below to complete verification</p><a href='{url}'>Verify</a></body></html>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
    except:
        pass

    return True

def verify_secret_key(secret_key):

    try:
        obj = EV.objects.get(secret_key=secret_key)
        if obj.has_expired is not True:
            return (True,obj.user)
        else:
            return (False,None)
    except:
        return (False,None)

def send_notification(user,msg,url,category="general"):
    notification = Notification.objects.create(user=user,message=msg,category=category,url=url)
    return True

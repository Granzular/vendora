#
import uuid
from django.shortcuts import reverse

def send_confirmation_email(email):

    secret_key = "vendora"+ str(uuid.uuid4())
    url = reverse("customers:verify_email", kwargs={"secret_key":secret_key})
    print(url)
    #send the email here

    return secret_key

import requests
import os
class PaystackClient:
    BASE_URL = "https://api.paystack.co"
    VALID_STATUSES = {
            "success": "success",
            "failed": "failed",
            "abandoned": "abandoned",
            "processing": "processing",
            "reversed": "reversed",
            }
    SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.SECRET_KEY}",
            "Content-Type": "application/json",
        }

    def initialize_payment(self, email, amount, **kwargs):
        """Start a payment process"""
        url = f"{self.BASE_URL}/transaction/initialize"
        data = {"email": email, "amount":int( amount*100)}
        data.update(kwargs)
        r = requests.post(url, json=data, headers=self.headers)
        return r.json()

    def verify_payment(self, reference):
        """Confirm payment after user checkout"""
        url = f"{self.BASE_URL}/transaction/verify/{reference}"
        r = requests.get(url, headers=self.headers)
        return r.json()
    
    def get_status(self,status_string):
        return self.VALID_STATUSES.get(status_string, "unknown")


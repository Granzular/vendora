import requests

class PaystackClient:
    BASE_URL = "https://api.paystack.co"

    def __init__(self, secret_key):
        self.headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }

    def initialize_payment(self, email, amount, **kwargs):
        """Start a payment process"""
        url = f"{self.BASE_URL}/transaction/initialize"
        data = {"email": email, "amount": amount}
        data.update(kwargs)
        r = requests.post(url, json=data, headers=self.headers)
        return r.json()

    def verify_payment(self, reference):
        """Confirm payment after user checkout"""
        url = f"{self.BASE_URL}/transaction/verify/{reference}"
        r = requests.get(url, headers=self.headers)
        return r.json()

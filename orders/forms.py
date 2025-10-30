from django import forms

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=50,widget=forms.TextInput({"required":"true"}))
    last_name = forms.CharField(max_length=50,widget=forms.TextInput({"required":"true"}))
    email = forms.EmailField(max_length=150,widget=forms.EmailInput({"required":"true"}))
    phone = forms.IntegerField(widget=forms.TelInput({"required":"true"}))
    delivery_address = forms.CharField(max_length=150,widget=forms.TextInput({"required":"true"}))




from django import forms

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=120, label="Full Name")
    phone = forms.CharField(max_length=30, label="Phone Number")
    address = forms.CharField(widget=forms.Textarea, label="Address")

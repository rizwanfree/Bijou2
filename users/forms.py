from django import forms
from django.contrib.auth.models import User

class TenantRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    first_name = forms.CharField(max_length=50)
    middle_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
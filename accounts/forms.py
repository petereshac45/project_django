from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True) 
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'user name ',
            'password1': 'Password',
            'password2': 'confirm password',
            'email': 'Email',
        }
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
            'email': None,
        }
